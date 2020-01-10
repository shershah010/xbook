import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='Pizza.network1',
                             port=3307,
                             db='xbook')
cursor = connection.cursor()
cursor.execute('USE xbook;')

def getToken(username, password):
    sql = """
        SELECT token FROM Users
        WHERE username=%s
        AND password=%s
    """
    cursor.execute(sql, (username, password))
    results = cursor.fetchone()
    if results is None:
        return None
    return results[0] # returns the token
