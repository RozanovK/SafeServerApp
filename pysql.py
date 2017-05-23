import pymysql
import hashlib



def checkAuth(login, passwd):
        db = pymysql.connect("localhost","rozanovk","siema","login")
        cursor = db.cursor()
        cursor.execute('SELECT password FROM users WHERE login = %s', login)
        results = str(cursor.fetchone()[0])
        db.close()
        password = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        if results == password:
            return True
        else:
            return False


if __name__ == "__main__":
    if checkAuth('rozanovk', 'siema'):
        print('Autoryzacja poszła pomyślnie')
    else:
        print('What')

