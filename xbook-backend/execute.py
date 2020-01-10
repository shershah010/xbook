def execute_helper(request):
    if request is None or request.json['command'] is None:
        return {'response': 'NO COMMAND'}, 400
    command = request.json['command']
    response, status = execute_helper_not_none(command)
    return response, status

def execute_helper_not_none(command):
    return get_response(clean_command(command))

def clean_command(input):
    return input.strip()

def get_response(command):
    if command == 'login':
        return {'response': 'login'}, 200
    elif command == 'register':
        pass
    elif command == 'aboutme':
        pass
    elif command == 'friends':
        pass
    elif command == 'messages':
        pass
    elif command == 'posts':
        pass
    else:
        return {'response': 'BAD COMMAND'}, 200
