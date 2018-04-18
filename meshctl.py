from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from sqlalchemy import create_engine
from json import dumps
import json
from flask_cors import CORS
from flask import Flask, request, render_template
import time
import pexpect
import subprocess
import sys

db_connect = create_engine('sqlite:///database.db') #create_engine("mysql://mesh:1234@138.68.161.169/mesh", pool_recycle=3600)
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

class MeshError(Exception):
    """Wywołano ponieważ wystąpił błąd w meshctl."""
    pass


class Meshctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("./meshctl", echo = False)    		
    '''UWAGA! Wykomentowanie self.child =(...)do testow sprawi, ze'''
    '''devices.json nie bedzie usuwany przy starcie,              '''
    
    
    '''Dodać wyświetlanie logów z konsoli'''
    '''Dodać argumenty który TARGET'''
    '''Zbudować z tego api'''
    def prov_device(self):
        """Provision device"""
        self.child.send("discover-unprovisioned on" + "\n") #Tutaj raczej nie potrzebne
        time.sleep(20)
        self.child.send("security 0" + "\n")
        time.sleep(1)
        self.child.send("provision e6053641e8e200000000000000000000" + "\n")
        time.sleep(10)
        self.child.send("menu config" + "\n")
        time.sleep(1)
        self.child.send("target 0100" + "\n")
        time.sleep(1)
        self.child.send("appkey-add 1" + "\n")
        time.sleep(1)
        self.child.send("bind 0 1 1000" + "\n")
        time.sleep(1)
        self.child.send("sub-add 0100 c000 1000" + "\n")
        
        time.sleep(1)
        return "Provisioned!"
        
    def provision(self, device_name, uuid, address):
        #Wyslanie polecenia meshctl
        self.child.send("security 0" + "\n")
        time.sleep(1)
        self.child.send("provision " + uuid + "\n")
        time.sleep(12)
        
        #Otwarcie pliku z danymi przeslanymi przez nrf
        file = open("prov_db.json", 'r')
        content = file.read()
        content= "{\"data\":[" + content + "]}"
        content = json.loads(content)     
        unicastAddress = content['data'][-1]['nodes'][-1]['configuration']['elements'][-1]['unicastAddress']
        
        #Uzupelnienie bazy danych o dane z pliku
        query_string = "INSERT INTO devices (id, address, name, state, target, uuid)"
        query_string += "VALUES (NULL, NULL, \"zephyr\", 0,"
        query_string += unicastAddress + ", \"" + uuid + "\" )"
        conn = db_connect.connect()
        query = conn.execute(query_string)
        
        return 0
    
    '''Przemyśleć to czy właściwie jest potrzebne'''
    '''Właściwie powinno to być w inicjalizacji całej usługi'''
    '''Dodać argumenty który TARGET'''
    '''Zbudować z tego api'''   
    def start_scan(self):
        self.child.send("discover-unprovisioned on" + "\n")
        time.sleep(20)
        
    '''Dodać wyświetlanie logów z konsoli'''
    '''Dodać argumenty który TARGET'''
    '''Zbudować z tego api'''
    def init_led(self,):
        """Change led state"""
        self.child.send("back" + "\n")
        time.sleep(1)
        self.child.send("menu onoff" + "\n")
        time.sleep(1)
        self.child.send("target 0100" + "\n")
        time.sleep(1)
        return "Led Init OK!"
        
    def led_on(self):                       #dodać argument UUID
        """Change led state"""              #zbudować z tego api
        self.child.send("onoff 1" + "\n")
        time.sleep(1)
        return "LED On!"
    
    def led_off(self):                      #dodać argument UUID
        """Change led state"""              #zbudować z tego api
        self.child.send("onoff 0" + "\n")
        time.sleep(1)
        return "LED Off!"
    
class test_provisioning(Resource):
    def get(self):
        uuid = "129381241298714edfa"
        file = open("prov_db.json", 'r')
        content = file.read()
        content= "{\"data\":[" + content + "]}"
        content = json.loads(content)     
        unicastAddress = content['data'][-1]['nodes'][-1]['configuration']['elements'][-1]['unicastAddress']
        #Uzupelnienie bazy danych o dane z pliku
        query_string = "INSERT INTO devices (id, address, name, state, target, uuid)"
        query_string += "VALUES (NULL, NULL, \"zephyr\", 0,"
        query_string += unicastAddress + ", \"" + uuid + "\" )"
        conn = db_connect.connect()
        query = conn.execute(query_string)
        
        return unicastAddress

class UserList(Resource):
    def post(self):
        conn = db_connect.connect()
        query = conn.execute("select * from user;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
    
class login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        ln = json_data['login']
        pw = json_data['pass']
        conn = db_connect.connect()
        query = conn.execute('select email, login, name, surname, url from user WHERE login = "%s" and password = "%s";' % (ln, pw))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class blescan(Resource):
    def get(self):
        file=open("devices.json",'r')
        content=file.read()
        content= "{\"devices\":[" + content + "]}"
        content = json.loads(content)
        file.close()
        return content

class addlight(Resource):                           #Tutaj całość do poprawy: 
    def post(self):                                 #1)Zmienić DB
        json_data = request.get_json(force=True)    #2)Zaimplementować Provisoring
        ad = json_data['address']                   #3)Inicalizacja LED
        nm = json_data['name']
        st = "0"
        print("ad")
        conn = db_connect.connect()
        query = conn.execute("insert into devices values(null,'{0}','{1}','{2}')".format(ad,nm,st))
        print ("test")
        return {'status':'success'}
    
class devicelist(Resource):
    def post(self):
        conn = db_connect.connect()
        query = conn.execute("select * from devices;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
    
    
#logowanie
api.add_resource(UserList, '/api/login_all') # Zwraca liste wszystkich userow
api.add_resource(login, '/api/login') # Zwraca dane pojedynczego usera, sprawdza logowanie!!! /TODO
#wyszukiwanie
api.add_resource(blescan, '/api/blescan') # Zwraca liste ble w otoczeniu
api.add_resource(addlight, '/api/addlight') # Dodaje plytke do bazy
api.add_resource(devicelist, '/api/devices') # Zwraca liste wszystkich urzadzen
#hece z plytka
#api.add_resource(writeled, '/writeled') #Zapala leda na NRF 
api.add_resource(test_provisioning, '/api/test_provisioning') #Do testowania 

if __name__ == '__main__':
    print("Init mshctl...")
    bl = Meshctl()
    print("Ready!")
    app.run(host = '127.0.0.1',port=5502)
    
    '''
    Rozumiem zrobić api jako:
    1) Stworzyć argument który będziemy wprowadzać
    <adres_ip>:<port>/api/NASZA_FUNKCJA_API/<parametr>
    2)Zrobić return w jsonie
    Status: success albo parametr który uzyskaliśmy
    '''



