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
    message = ' '.join(cmd_array[len(args) + 1:])
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
        return {'response': handle_friend(token, args, message, db)}, 200
    elif command == 'messages':
        return {'response': handle_message(token, args, message, db)}, 200
    elif command == 'posts':
        return {'response': handle_post(token, args, message, db)}, 200
    elif command == 'comments':
        return {'response': handle_comment(token, args, message, db)}, 200
    else:
        return {'response': 'BAD COMMAND'}, 200

def handle_message(token, args, message, db):
    if '-c' in args:
        destination = message.split(' ')[0]
        message = ' '.join(message.split(' ')[1:])
        return db.create_message(token, destination, message)
    elif '-r' in args:
        return db.read_message(token, message)
    elif '-u' in args:
        id = message.split(' ')[0]
        message = ' '.join(message.split(' ')[1:])
        return db.update_message(token, id, message)
    elif '-d' in args:
        return db.delete_message(token, message)
    else:
        return db.read_message(token, '*')

def handle_post(token, args, message, db):
    if '-c' in args:
        return db.create_post(token, message)
    elif '-r' in args:
        return db.read_post(message, is_token=False)
    elif '-u' in args:
        id = message.split(' ')[0]
        message = ' '.join(message.split(' ')[1:])
        return db.update_post(token, id, message)
    elif '-d' in args:
        return db.delete_post(token, id)
    else:
        return db.read_post(token, is_token=True)

def handle_comment(token, args, message, db):
    id = message.split(' ')[0]
    message = ' '.join(message.split(' ')[1:])
    if '-c' in args:
        return db.create_comment(token, id, message)
    elif '-r' in args:
        return db.read_comment(id)
    elif '-u' in args:
        return db.update_comment(token, id, message)
    elif '-d' in args:
        return db.delete_comment(token, id)
    else:
        return db.read_comment(id)

def handle_friend(token, args, username, db):
    if '-a' in args:
        return db.approve_friend(token, username)
    elif '-r' in args:
        return db.remove_friend(token, username)
    elif '-s' in args:
        return db.send_friend(token, username)
    else:
        return db.read_friend(token)
