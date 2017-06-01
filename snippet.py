from datetime import datetime
import pathlib



def getSnippet(headers, body, data, login):

    snippet = str(data['snippet']) if 'snippet' in data else ''

    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.now().strftime(f)
    filename = login + '.txt'
    file = open(filename, 'w')
    file.write(time + '\n')
    file.write(snippet + '\n')


def putSnippet(login):

    snippets = []
    datet = []
    def validate(d):
        try:
            datetime.strptime(d, "%Y-%m-%d %H:%M:%S\n")
            return True
        except ValueError:
            return False

    filename = login + '.txt'
    path = pathlib.Path(filename)
    if path.is_file():
        with open(filename, 'r') as f:
            for line in f:
                if validate(line):
                    datet.append(line)
                    print(datet[0])
                else:
                    snippets.append(line)
        print (snippets)


putSnippet('rozanovk')








