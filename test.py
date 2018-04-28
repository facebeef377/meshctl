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
import cleaner
    
file = open("prov_db.json", 'r')
content = file.read()
content= "{\"data\":[" + content + "]}"
content = json.loads(content)     
unicastAddress = content['data'][-1]['nodes'][-1]['configuration']['elements'][-4]['unicastAddress']
print(unicastAddress)