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

    def get_token(self, username, password):
        sql = """
            SELECT token, password FROM Users
            WHERE username=%s
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
        if not self.unique_user(username):
            return None
        sql = """
            INSERT INTO Users (token, firstname, lastname, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        token = secrets.token_hex(32)
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.cursor.execute(sql, (token, firstname, lastname, username, hashed_password))
        return 'success'

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

    def unique_user(self, username):
        sql = """
            SELECT * FROM Users
            WHERE username=%s
        """
        self.cursor.execute(sql, (username,))
        results = self.cursor.fetchall()
        return results is None or results is () or len(results) == 0

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
        if not self.unique_user(destination):
            return 'FAILURE'
        sql = """
            INSERT INTO Messages (origin, destination, message)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (username, destination, message))
        return 'SUCCESS'

  # mysql -uroot -p -h 35.247.63.129 --ssl-ca=./ssl_certificates/server-ca.pem --ssl-cert=./ssl_certificates/client-cert.pem --ssl-key=./ssl_certificates/client-key.pem
