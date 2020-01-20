import pymysql
import secrets
import bcrypt

class Database_Manager():
    def __init__(self):
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='Pizza.network1',
                                     port=3307,
                                     db='xbook',
                                     autocommit=True)
        self.cursor = connection.cursor()
        self.cursor.execute('USE xbook;')

    def sql_pretty_display(self, header, sql_output):
        sql_output = [[x for x in xs] for xs in sql_output]
        sql_output.insert(0, header)
        col_width = max([max([len(str(word)) for word in row]) for row in sql_output]) + 2  # padding
        pretty_output = ''
        for row in sql_output:
            pretty_output += "".join(str(word).ljust(col_width) for word in row) + '\n'
        return pretty_output

    def get_token(self, username, password):
        sql = """
            SELECT token, password FROM Users
            WHERE username = %s
        """
        self.cursor.execute(sql, (username,))
        results = self.cursor.fetchone()
        if results is None:
            return None
        if bcrypt.checkpw(password.encode('utf8'), results[1].encode('utf8')):
            return results[0] # returns the token
        else:
            return None

    def create_user(self, firstname, lastname, username, password):
        if not self.unique_user(username, 0):
            return None
        sql = """
            INSERT INTO Users (token, firstname, lastname, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        token = secrets.token_hex(32)
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.cursor.execute(sql, (token, firstname, lastname, username, hashed_password))
        return token

    def get_username(self, token):
        if token is None:
            return 'Permission denied'
        sql = """
            SELECT username FROM Users
            WHERE token=%s
        """
        self.cursor.execute(sql, (token,))
        results = self.cursor.fetchone()
        if results is None:
            return 'Permission denied'
        return results[0] # returns the username

    def unique_user(self, username, free=0):
        sql = """
            SELECT * FROM Users
            WHERE username=%s
        """
        self.cursor.execute(sql, (username,))
        results = self.cursor.fetchall()
        return len(results) == free

    def logout(self, token):
        if token is None:
            return 'not logged in'
        self.update_token(token)
        return 'logout'

    def update_token(self, token):
        sql = """
            UPDATE Users
            SET token = %s
            WHERE token = %s
        """
        secret = secrets.token_hex(32)
        self.cursor.execute(sql, (secret, token))
        return secret

    def create_message(self, token, destination, message):
        username = self.get_username(token)
        if username == 'Permission denied':
            return 'FAILURE'
        if not self.unique_user(destination, 1):
            return 'FAILURE'
        sql = """
            INSERT INTO Messages (origin, destination, message)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (username, destination, message))
        return 'SUCCESS'

    def read_message(self, token, id):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            SELECT * FROM Messages
            WHERE origin = %s
            OR destination = %s
        """
        if id != '*':
            sql += 'AND id = %s'
            self.cursor.execute(sql, (username, username, int(id, base=10)))
        else:
            self.cursor.execute(sql, (username, username))
        header = ['id', 'sender', 'reciever', 'message']
        return self.sql_pretty_display(header, self.cursor.fetchall())

    def update_message(self, token, id, message):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            UPDATE Messages
            SET message = %s
            WHERE origin = %s
            AND id = %s
        """
        self.cursor.execute(sql, (message, username, int(id, base=10)))
        return 'SUCCESS'

    def delete_message(self, token, id):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            DELETE FROM Messages
            WHERE origin = %s
            AND id = %s
        """
        self.cursor.execute(sql, (username, int(id, base=10)))
        return 'SUCCESS'

    def create_post(self, token, message):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            INSERT INTO Posts (origin, message)
            VALUES (%s, %s)
        """
        self.cursor.execute(sql, (username, message))
        return 'SUCCESS'

    def read_post(self, id, is_token=False):
        if is_token:
            id = self.get_username(id)
        if not self.unique_user(id, 1):
            return 'FAILURE'
        sql = """
            SELECT * FROM Posts
            WHERE origin = %s
        """
        self.cursor.execute(sql, (id,))
        header = ['id', 'origin', 'message']
        return self.sql_pretty_display(header, self.cursor.fetchall())

    def update_post(self, token, id, message):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            UPDATE Posts
            SET message = %s
            WHERE origin = %s
            AND id = %s
        """
        self.cursor.execute(sql, (message, username, int(id, base=10)))
        return 'SUCCESS'

    def delete_post(self, token, id):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            DELETE FROM Posts
            WHERE origin = %s
            AND id = %s
        """
        self.cursor.execute(sql, (username, int(id, base=10)))
        return 'SUCCESS'

    def create_comment(self, token, post_id, message):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            INSERT INTO Comments (origin, post_id, message)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (username, int(post_id, 10), message))
        return 'SUCCESS'

    def read_comment(self, id):
        sql = """
            SELECT * FROM Comments
            WHERE post_id = %s
        """
        self.cursor.execute(sql, (int(id, 10),))
        return self.sql_pretty_display(self.cursor.fetchall())

    def update_comment(self, token, id, message):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            UPDATE Comments
            SET message = %s
            WHERE username = %s
            AND id = %s
        """
        self.cursor.execute(sql, (message, username, int(id, 10)))
        return 'SUCCESS'

    def delete_comment(self, token, id):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            DELETE FROM Comments
            WHERE origin = %s
            AND id = %s
        """
        self.cursor.execute(sql, (username, int(id, 10)))
        return 'SUCCESS'

    def approve_friend(self, token, friend):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            SELECT * FROM Friends
            WHERE accepted = 0
            AND origin = %s
            and destination = %s
        """
        self.cursor.execute(sql, (friend, username))
        results = self.cursor.fetchall()
        if len(results) != 1:
            return 'FAILURE'
        sql = """
            UPDATE Friends
            SET accepted = 1
            WHERE origin = %s
            AND destination = %s
        """
        self.cursor.execute(sql, (friend, username))
        sql = """
            INSERT INTO Friends (origin, destination, accepted)
            VALUES (%s, %s, 1)
        """
        self.cursor.execute(sql, (username, friend))
        return 'SUCCESS'

    def remove_friend(self, token, friend):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            DELETE FROM Friends
            WHERE ((origin = %s
            AND destination = %s)
            OR (destination = %s
            AND origin = %s))
            AND accepted = 1
        """
        self.cursor.execute(sql, (username, friend, username, friend))
        return 'SUCCESS'

    def send_friend(self, token, friend):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            INSERT INTO Friends (origin, destination, accepted)
            VALUE (%s, %s, 0)
        """
        self.cursor.execute(sql, (username, friend))
        return 'SUCCESS'

    def read_friend(self, token):
        username = self.get_username(token)
        if not self.unique_user(username, 1):
            return 'FAILURE'
        sql = """
            SELECT * FROM Friends
            WHERE origin = %s
            OR destination = %s
        """
        self.cursor.execute(sql, (username, username))
        header = ['sender', 'reciever', 'accepted']
        return self.sql_pretty_display(header, self.cursor.fetchall())

  # mysql -uroot -p -h 35.247.63.129 --ssl-ca=./ssl_certificates/server-ca.pem --ssl-cert=./ssl_certificates/client-cert.pem --ssl-key=./ssl_certificates/client-key.pem
