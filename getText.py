import os
import sys
import subprocess

if not os.path.isdir('data/text'):
        os.mkdir('data/text')

badFiles = []
noAdjudged = []

for fileName in os.listdir('data/raw'):
    fileName = fileName[:-4]

    subprocess.run(['gs','-sDEVICE=txtwrite', '-o', 'data/text/' + fileName + '.txt', 'data/raw/' + fileName + '.pdf'])

    print('Starting trimming for ' + fileName)
    fi = open('data/text/' + fileName + '.txt', 'r', errors='ignore')
    text = fi.readlines()

    checkStr = text[1].strip('\t \n')
    if 'INDEX' in checkStr or 'ORDERS' in checkStr:
        print("BAD FILE:", fileName)
        fi.close()
        subprocess.run(['rm', 'data/text/' + fileName + '.txt'])
        badFiles.append(fileName)
        continue

    start = -1
    for i in range(len(text)):
        if 'ADJUDGED' in text[i].replace(' ', '').replace(' ', '').strip('  \n\t'):
            start = i
    if start < 0:
        noAdjudged.append(fileName)

    text = ' '.join(list(map(lambda line: line.strip('\t \n'), text[start+1:])))

    # Find stop index
    stop = max([text.find('ORDERS FOR'), text.find('ORDERS FOR'), text.find('ORDERSFOR')]) # yes those are different
    fi.close()

    fi = open('data/text/' + fileName + '.txt', 'w')
    fi.write(text[:stop])
    fi.close()

print('\nSummary:')
print('\tBad Files:', badFiles)
print('\tNo Adjudged, but OK:', noAdjudged)


