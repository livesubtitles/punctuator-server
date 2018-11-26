# import httplib2
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from punctuate import *
from punctuator2.punctuator import *
from apiclient import discovery
from oauth2client import client

app = Flask(__name__)
CORS(app, resources={r"/punctuate": {"origins": "*"}, "/storeauthcode":{"origins":"*"}})

first_request = True

def prepare_model_file():
    f1 = open("./punctuator2/model1.pcl", "rb")
    final_file = open("./punctuator2/final-model.pcl", "wb")
    for line in f1:
        final_file.write(line)
    f1.close()
    print("Writing first file completed")
    f2 = open("./punctuator2/model2.pcl", "rb")
    for line in f2:
        final_file.write(line)
    f2.close()
    print("Writing second file completed")
    final_file.close()

@app.route("/")
def index():
    return "Hello"
@app.route("/punctuate", methods=['POST'])
def punctuate():
    global first_request
    if (first_request):
        if (not os.path.isfile("./punctuator2/final-model.pcl")):
            prepare_model_file()
        model_path = "./punctuator2/final-model.pcl"
        init_punctuator(model_path)
        first_request = False
    request_body = json.loads(request.data)
    subtitle = request_body['subtitle']
    return jsonify(subtitle=punctuate_subtitle(subtitle))
