import httplib2
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

@app.route("/oauth")
def oauth():
	return send_file('oauth.html')

@app.route("/storeauthcode", methods=['POST'])
def get_user_access_token_google():
	auth_code = str(request.data).split("\'")[1]
	# If this request does not have `X-Requested-With` header, this could be a CSRF
	if not request.headers.get('X-Requested-With'):
	    abort(403)
	# Set path to the Web application client_secret_*.json file you downloaded from the
	# Google API Console: https://console.developers.google.com/apis/credentials
	CLIENT_SECRET_FILE = 'client_secret_1070969009500-4674ntngjh3dvlbcvoer0r4c7hao04dh.apps.googleusercontent.com.json'

	# Exchange auth code for access token, refresh token, and ID token
	credentials = client.credentials_from_clientsecrets_and_code(
	    CLIENT_SECRET_FILE,
	    ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
	    auth_code)

	# Call Google API
	http = httplib2.Http()
	http_auth = credentials.authorize(http)
	resp, content = http.request(
        'https://www.googleapis.com/language/translate/v2/?q=voiture&target=en&source=fr')
	print(resp.status)
	print(content.decode('utf-8'))
	# drive_service = discovery.build('drive', 'v3', http=http_auth)
	# appfolder = drive_service.files().get(fileId='appfolder').execute()

	# Get profile info from ID token
	userid = credentials.id_token['sub']
	email = credentials.id_token['email']
	print(userid)
	print(email)
	return ""
