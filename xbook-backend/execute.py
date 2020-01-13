def execute_helper(request, db):
    if request is None or request.json['command'] is None:
        return {'response': 'NO COMMAND'}, 400
    command = request.json['command']
    token = request.json['token']
    response, status = execute_helper_not_none(command, token, db)
    return response, status

def execute_helper_not_none(command, token, db):
    return get_response(clean_command(command), token, db)

def clean_command(input):
    return input.strip()

def get_response(command, token, db):
    if command == 'register':
        pass
    elif command == 'aboutme':
        return {'response': db.about_me(token)}, 200
    elif command == 'friends':
        pass
    elif command == 'messages':
        pass
    elif command == 'posts':
        pass
    else:
        return {'response': 'BAD COMMAND'}, 200
