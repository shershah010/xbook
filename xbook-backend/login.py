from db import *

def login_helper(request):
    if request is None or request.json['username'] is None or request.json['password'] is None:
        return {'response': 'FAILURE'}, 400
    username = request.json['username']
    password = request.json['password']
    return login_helper_not_none(username, password)

def login_helper_not_none(username, password):
    token = getToken(username, password)
    if token is None:
        return {'response': 'FAILURE'}, 200
    return {'response': 'SUCCESS', 'token': token}, 200

  # mysql -uroot -p -h 35.247.63.129 \
  #   --ssl-ca=./ssl_certificates/server-ca.pem --ssl-cert=./ssl_certificates/client-cert.pem \
  #   --ssl-key=./ssl_certificates/client-key.pem
