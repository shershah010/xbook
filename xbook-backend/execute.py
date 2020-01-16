def execute_helper(request, db):
    if request is None or request.json['command'] is None:
        return {'response': 'NO COMMAND'}, 400
    command = request.json['command']
    try:
        token = request.json['token']
    except:
        token = None
    response, status = execute_helper_not_none(command, token, db)
    return response, status

def execute_helper_not_none(command, token, db):
    return get_response(clean_command(command), token, db)

def clean_command(input):
    cmd_array = input.strip().split(' ')
    if len(cmd_array) == 0:
        return None
    name = cmd_array[0]
    args = [token for token in cmd_array[1:] if token[0] == '-']
    message = ''
    for token in cmd_array[len(args):]:
        message += token
    return (name.lower(), args, message)

def get_response(command_package, token, db):
    if command_package is None:
        return {'response': 'BAD COMMAND'}, 200
    command, args, message = command_package
    if command == 'logout':
        return {'response': db.logout(token)}, 200
    elif command == 'aboutme':
        return {'response': db.get_username(token)}, 200
    elif command == 'friends':
        pass
    elif command == 'message':
        return {'response': self.message(token, args, message)}, 200
    elif command == 'posts':
        pass
    else:
        return {'response': 'BAD COMMAND'}, 200

def message(token, args, message):
    if args == '-c':
        destination = message.split(' ')[0]
        message = ' '.join(message.split(' ')[1:])
        return db.create_message(token, destination, message)
    elif args == '-r':
        return db.read_message(token, message)
    elif args == '-u':
        id = message.split(' ')[0]
        message = ' '.join(message.split(' ')[1:])
        return db.update_message(token, id, message)
    elif args == '-d':
        return db.delete_message(token, message)
