def register_helper(request, db):
    if request is None or \
    request.json['username'] is None or \
    request.json['password'] is None or \
    request.json['firstname'] is None or \
    request.json['lastname'] is None:
        return {'response': 'FAILURE'}, 400
    username = request.json['username']
    password = request.json['password']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    return register_helper_not_none(username, password, firstname, lastname, db)

def register_helper_not_none(username, password, firstname, lastname, db):
    token = db.create_user(firstname, lastname, username, password)
    if token is None:
        return {'response': 'FAILURE', 'flag': 0}, 200
    return {'response': 'SUCCESS', 'flag': 2, 'token': token}, 200
