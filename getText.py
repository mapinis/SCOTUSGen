import os
import sys
import subprocess

if not os.path.isdir('data/text'):
        os.mkdir('data/text')

badFiles = []
noAdjudged = []

for fileName in os.listdir('./data/raw'):
    fileName = fileName[:-4]

    subprocess.run(['gs','-sDEVICE=txtwrite', '-o', 'data/text/' + fileName + '.txt', 'data/raw/' + fileName + '.pdf'])

    print('Starting trimming for ' + fileName)
    fi = open('data/text/' + fileName + '.txt', 'r', errors='ignore')
    text = fi.readlines()

    if text[1].strip('\t \n') == 'INDEX':
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
        # rm here?
        continue

    text = ' '.join(list(map(lambda line: line.strip('\t \n'), text[start+1:])))
    '''# Find start indexsys.exit('Cases Adjudged not found')
    # Case 1: First instance words together
    te = text.replace('CASESADJUDGED', '', 1)
    starts = [
        te.find('CASESADJUDGED'), # Case A: Second instance words together
        te.find('CASES ADJUDGED') # Case B: Second instance words seperate
    ]
    # Case 2: First instance words seperate
    te = text.replace('CASES ADJUDGED', '', 1)
    starts += [
        te.find('CASESADJUDGED'), # Case A
        te.find('CASES ADJUDGED') # Case B
    ]
    start = max(starts) + 66'''

    # Find stop index
    stop = max([text.find('ORDERS FOR'), text.find('ORDERS FOR'), text.find('ORDERSFOR')]) # yes those are different
    fi.close()

    fi = open('data/text/' + fileName + '.txt', 'w')
    fi.write(text[:stop])
    fi.close()

print('\nSummary:')
print('\tBad Files:', badFiles)
print('\tNo Adjudged:', noAdjudged)


