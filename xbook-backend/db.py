import pymysql

class Database_Manager():
    def __init__(self):
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='Pizza.network1',
                                     port=3307,
                                     db='xbook')
        self.cursor = connection.cursor()
        self.cursor.execute('USE xbook;')

    def get_token(self, username, password):
        sql = """
            SELECT token FROM Users
            WHERE username=%s
            AND password=%s
        """
        self.cursor.execute(sql, (username, password))
        results = self.cursor.fetchone()
        if results is None:
            return None
        return results[0] # returns the token

    def about_me(self, token):
        if token is None:
            return None
        sql = """
            SELECT username FROM Users
            WHERE token=%s
        """
        self.cursor.execute(sql, (token,))
        results = self.cursor.fetchone()
        if results is None:
            return None
        return results[0] # returns the username

  # mysql -uroot -p -h 35.247.63.129 \
  #   --ssl-ca=./ssl_certificates/server-ca.pem --ssl-cert=./ssl_certificates/client-cert.pem \
  #   --ssl-key=./ssl_certificates/client-key.pem
