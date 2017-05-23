from pysql import checkAuth

if __name__ == "__main__":
    if checkAuth('rozanovk', 'siema'):
        print('Autoryzacja poszła pomyślnie')
    else:
        print('Złe hasło')