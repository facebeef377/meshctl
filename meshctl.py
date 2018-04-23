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
import ast

db_connect = create_engine('sqlite:///database.db') #create_engine("mysql://mesh:1234@138.68.161.169/mesh", pool_recycle=3600)
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

class MeshError(Exception):
    """Error running meshctl."""
    pass


class Meshctl:
    """A wrapper for meshctl utility."""

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("./meshctl", echo = False) 
        time.sleep(1)
        self.child.send("discover-unprovisioned on" + "\n")
    
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
        
    def provision(self, uuid):
        #Wyslanie polecenia meshctl
        self.child.send("security 0" + "\n")
        time.sleep(1)
        self.child.send("provision " + uuid + "\n")
        time.sleep(12)
        file = open("prov_db.json", 'r')
        content = file.read()
        content= "{\"data\":[" + content + "]}"
        content = json.loads(content)     
        unicastAddress = content['data'][-1]['nodes'][-1]['configuration']['elements'][-1]['unicastAddress']
        print unicastAddress
        
        self.child.send("menu config" + "\n")
        time.sleep(1)
        self.child.send("target " + unicastAddress + "\n")
        time.sleep(1)
        self.child.send("appkey-add 1" + "\n")
        time.sleep(1)
        self.child.send("bind 0 1 1000" + "\n")
        time.sleep(1)
        self.child.send("sub-add " + unicastAddress + " c000 1000" + "\n")
        time.sleep(1)
        self.child.send("back" + "\n")
        time.sleep(1)
        
        return unicastAddress
        
    def init_led(self, target):
        self.child.send("menu config" + "\n")
        time.sleep(1)
        self.child.send("target " + target + "\n")
        time.sleep(1)
        self.child.send("appkey-add 1" + "\n")
        time.sleep(1)
        self.child.send("bind 0 1 1000" + "\n")
        time.sleep(1)
        self.child.send("sub-add " + target + " c000 1000" + "\n")
        time.sleep(1)
        self.child.send("back" + "\n")
        return "Led Init OK!"
    
        
    def led_on(self, target):
        """Change led state"""
        self.child.send("menu onoff" + "\n")
        time.sleep(1)
        self.child.send("target " + target + "\n")
        time.sleep(1)
        self.child.send("onoff 1" + "\n")
        time.sleep(1)
        self.child.send("back" + "\n")
        time.sleep(1)
        return "LED On!"
    
    def led_off(self, target):
        self.child.send("menu onoff" + "\n")
        time.sleep(1)
        self.child.send("target " + target + "\n")
        time.sleep(1)
        self.child.send("onoff 0" + "\n")
        time.sleep(1)
        self.child.send("back" + "\n")
        time.sleep(1)
        return "LED On!"
    

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
    def post(self):
        file=open("devices.json",'r')
        content=file.read()
        file.close()
        data_dict = ast.literal_eval(content)
        return {'devices' : data_dict}
    
    def get(self):
        file=open("devices.json",'r')
        content=file.read()
        file.close()
        data_dict = ast.literal_eval(content)
        return {'devices' : data_dict}

class addlight(Resource): 
    def post(self):                                 #1)Zmienic DB
        json_data = request.get_json(force=True)    #2)Zaimplementowac Provisoring
        ad = json_data['address']                   #3)Inicalizacja LED
        nm = json_data['name']
        st = "0"
        print("ad")
        conn = db_connect.connect()
        query = conn.execute("insert into devices values(null,'{0}','{1}','{2}')".format(ad,nm,st))
        print ("test")
        return {'status' : 'OK'}
    
class devicelist(Resource):
    def post(self):
        conn = db_connect.connect()
        query = conn.execute("select * from devices;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
    
class conn(Resource):
    def post(self):
        print("Init mshctl...")
        if(ifConnected == 0):
            global bl
            global ifConnected
            bl = Meshctl()
            ifConnected = 1
            return {'status' : 'OK'}
        return {'status' : 'error'}
        
class disconnect(Resource):
    def post(self):
        #Dopisac funckcje od zamykania mesha
        global ifConnected
        ifConnected = 0
        return {'status' : 'OK'}
        
class checkconnection(Resource):
    def post(self):
        if(ifConnected == 1):
            return {'status' : 'conn'}
        if(ifConnected == 0):
            return {'status' : 'none'}
        
class turn_on(Resource):
    def post(self):
        #Zmienic w bazie
        json_data = request.get_json(force=True)
        target = json_data['target']
        bl.led_on(target)
        return {'status' : 'OK'}
    
    def get(self):
        #Zmienic w bazie
        json_data = request.get_json(force=True)
        target = json_data['target']
        bl.led_on(target)
        return {'status' : 'OK'}
        
class turn_off(Resource):
    def post(self):
        #Zmienic w bazie
        json_data = request.get_json(force=True)
        target = json_data['target']
        bl.led_off(target)
        return {'status' : 'OK'}
    
    def get(self):
        #Zmienic w bazie
        json_data = request.get_json(force=True)
        target = json_data['target']
        bl.led_on(target)
        return {'status' : 'OK'}
        
class add_device(Resource):
    def post(self):
        #Zmienic w bazie
        json_data = request.get_json(force=True)
        uuid = json_data['uuid']
        device_name = json_data['name']
        address = json_data['address']
        device_type = "LED"
        state = "OFF"
        target = bl.provision(uuid)
        
        #Uzupelnienie bazy danych o dane z pliku
        conn = db_connect.connect()
        query = conn.execute("insert into devices values(null,'{0}','{1}','{2}','{3}','{4}','{5}')".format(device_name,uuid,target,address,device_type,state))
        
        return {'target' : target}
        
class set_device(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        device_type = json_data['type']
        #if(device_type = 'led')
        bl.init_led(target)
        return {'status' : 'OK'}
        #if(device_type == 'button')
        #    print "TODO"
        #    return {'status' : 'OK'}
        #return {'status' : 'error'}
        
        
#logowanie
api.add_resource(UserList, '/api/login_all') # Zwraca liste wszystkich userow
api.add_resource(login, '/api/login') # Zwraca dane pojedynczego usera, sprawdza logowanie!!! /TODO
#wyszukiwanie
api.add_resource(blescan, '/api/blescan') # Zwraca liste ble w otoczeniu
api.add_resource(addlight, '/api/addlight') # Dodaje plytke do bazy
api.add_resource(devicelist, '/api/devices') # Zwraca liste wszystkich urzadzen
#hece z plytka
api.add_resource(turn_on, '/api/on')            #Turn ON LED on nRF
api.add_resource(turn_off, '/api/off')           #Turn OFF LED on nRF
api.add_resource(add_device, '/api/add')         #Add nRF do mesh
#api.add_resource(set_device, '/api/set')         #Set device type
#meshctl-api
api.add_resource(conn, '/api/connect') #Connecting to proxy
api.add_resource(disconnect, '/api/disconnect') #Disconnecting from proxy
api.add_resource(checkconnection, '/api/checkconnection') #Checking connection to proxy

if __name__ == '__main__':
    ifConnected = 0
    bl = 0
    print("Ready!")
    app.run(host = '127.0.0.1',port=5502)
    

#Devices : Name, Address, UUID, Target ,State, Type
