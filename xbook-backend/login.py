def login_helper(request, db):
    if request is None or request.json['username'] is None or request.json['password'] is None:
        return {'response': 'FAILURE'}, 400
    username = request.json['username']
    password = request.json['password']
    return login_helper_not_none(username, password, db)

def login_helper_not_none(username, password, db):
    token = db.get_token(username, password)
    if token is None:
        return {'response': 'FAILURE'}, 400
    return {'response': 'SUCCESS', 'token': token}, 200
