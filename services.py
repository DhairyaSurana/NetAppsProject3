# Author: Dhairya Surana

# services.py

##################### INITIALIZATION ######################

# python3 services.py -p <WEBSERVER PORT>

###########################################################

#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
import os
import sys
import ServicesKeys
import requests

app = Flask(__name__)
auth = HTTPBasicAuth()

#################################### AUTHENTICATION ###########################################
@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'secret'
    return None

@auth.error_handler
def unauthorized():
    return make_response("  Could not verify your access level for that URL. \n  You have to login with the proper credentials.", 401)

##############################################################################################


@app.route('/Canvas', methods=['GET'])
@auth.login_required
def getCanvasInfo():

    # Get file URL
    file_name = request.args.get("file") 
    url = "https://vt.instructure.com/api/v1/courses/%s/files/?search_term=%s&access_token=%s" % ("104692", file_name, ServicesKeys.token)
    r = requests.get(url)  
    
    # Download file
    file_info = r.json()[0]
    download = requests.get(file_info["url"])
    open(file_info["filename"], 'wb').write(download.content)
    
    return r.text

@app.route('/Marvel', methods=['GET'])
@auth.login_required
def getMarvelInfo():

    # Get file URL
    story_name = request.args.get("story") 
    url = "http://gateway.marvel.com/v1/public/stories/%s?apikey=%s&hash=%s&ts=%s" % (story_name, ServicesKeys.apikey, ServicesKeys.hash, ServicesKeys.ts)
    r = requests.get(url)  
    
    open("Marvel.txt", 'wb').write(r.content) # Download file
    
    return r.text

@app.route('/goodbye', methods=['GET'])
@auth.login_required
def goodbye():
    return "Goodbye World"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':

    if(len(sys.argv) == 3 and sys.argv[1] == "-p"):

        try:
            app.run(port=sys.argv[2])
        except Exception as e:
            print(e)
    else:
        print("    Error: Incorrect args")
        print("    The format should be \"python3 services.py -p <WEBSERVER PORT>\"")