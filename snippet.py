import datetime


def getSnippet(headers, body, data, login):
    snippet = str(data['snippet']) if 'snippet' in data else ''

    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)
    filename = login + '.txt'
    file = open(filename, 'w')
    file.write(time + '\n')
    file.write(snippet + '\n')


