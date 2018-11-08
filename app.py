import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from punctuate import *
from punctuator2.punctuator import *

app = Flask(__name__)
CORS(app, resources={r"/punctuate": {"origins": "*"}})

first_request = True

@app.route("/punctuate", methods=['POST'])
def punctuate():
    global first_request
    if (first_request):
        model_path = "./punctuator2/final-model.pcl"
        init_punctuator(model_path)
        first_request = False
    request_body = json.loads(request.data)
    subtitle = request_body['subtitle']
    return jsonify(subtitle=punctuate_subtitle(subtitle))
