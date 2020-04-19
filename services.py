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

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

#################################### AUTHENTICATION ###########################################
@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'secret'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

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
    
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

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
        print("    Error: Incorrect args.\n    The format should be \"python3 services.py -p <WEBSERVER PORT>\"")