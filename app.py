from flask import Flask, request, jsonify
from flask_cors import CORS

from punctuate import *

app = Flask(__name__)
CORS(app, resources={r"/punctuate": {"origins": "*"}})

@app.route("/punctuate", methods=['POST'])
def punctuate():
    request_body = json.loads(request.data)
    subtitle = request_body['subtitle']
    return jsonify(subtitle=punctuate_subtitle(subtitle))
