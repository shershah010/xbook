from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import facebook
graph = facebook.GraphAPI(access_token="your_token", version="2.12")


app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return "Hello World!"

@app.route('/execute', methods=['POST'])
def execute():
    if ('execute' not in request.json.keys()):
        return jsonify({'response': 'BAD COMMAND'}), 400
    command = request.json['execute'];
    response, status = get_response(command)
    return {'response', response}, status

def get_response(command):
    return 'success', 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
