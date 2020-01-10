from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import re

from login import *
from execute import *

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})

@app.route('/execute', methods=['POST'])
def execute():
    response, status = execute_helper(request)
    return jsonify(response), status

@app.route('/login', methods=['POST'])
def login():
    response, status = login_helper(request)
    return jsonify(response), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
