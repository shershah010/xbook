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
        if bcrypt.checkpw(password, results[1]):
            return results[0] # returns the token
        else:
            return None

    def create_user(self, firstname, lastname, username, password):
        if self.not_unique_user(username):
            return None
        sql = """
            INSERT INTO Users (token, firstname, lastname, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        token = secrets.token_hex(32)
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.cursor.execute(sql, (token, firstname, lastname, username, hashed_password))
        return 'success'

    def about_me(self, token):
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

    def not_unique_user(self, username):
        sql = """
            SELECT * FROM Users
            WHERE username=%s
        """
        results = self.cursor.execute(sql, (username,))
        return results is None or len(results) == 0

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

  # mysql -uroot -p -h 35.247.63.129 \
  #   --ssl-ca=./ssl_certificates/server-ca.pem --ssl-cert=./ssl_certificates/client-cert.pem \
  #   --ssl-key=./ssl_certificates/client-key.pem
