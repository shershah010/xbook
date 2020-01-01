from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})

@app.route('/execute', methods=['POST'])
def execute():
    response, status = execute_helper(request.json['command'])
    return jsonify(response), status


def execute_helper(command):
    if command is None:
        return {'response': 'BAD COMMAND'}, 400
    response, status = get_response(command)
    return {'response': response}, status

def get_response(command):
    return 'success', 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
