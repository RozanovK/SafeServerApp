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

    snippets = ()
    datet = ()
    def validate(date_text):
        try:
            if date_text != datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S"):
                raise ValueError
            return True
        except ValueError:
            return False

    filename = login + '.txt'
    path = pathlib.Path('filename')
    if path.is_file():
        with open(filename, 'r') as f:
            for line in f:
                if validate(line):
                    datet[0] = line
                    snippets[line] = '\n'
                    print(datet[0] + '\n')
                else:
                    snippets[line] = line
                    print (snippets[line])


putSnippet('rozanovk')








