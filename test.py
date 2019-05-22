import os
import subprocess

if not os.path.isdir('data/text'):
        os.mkdir('data/text')

for fileName in os.listdir('./data/raw'):
    fileName = fileName[:-4]

    subprocess.run(['cmd', '/c', 'gswin64c -sDEVICE=txtwrite -o data/text/' + fileName + '.txt data/raw/' + fileName + '.pdf'])

    print(f'Starting trimming for {fileName}')
    fi = open('data/text/' + fileName + '.txt', 'r', errors='ignore')
    text = fi.readlines()
    text = ' '.join(list(map(lambda line: line.strip('\t \n'), text)))
    start = text.replace('CASESADJUDGED', '', 1).find('CASESADJUDGED') + 66
    stop = text.find('ORDERS FOR')
    fi.close()

    fi = open('data/text/' + fileName + '.txt', 'w')
    fi.write(text[start:stop])
    fi.close()

