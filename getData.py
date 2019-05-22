import os
import requests

def getData():
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('data/raw'):
        os.mkdir('data/raw')

    boundVolumesRange = map(str, range(502, 570)) # Start 502, Stop 570 for all volumes
    
    for boundVolume in boundVolumesRange:
        if os.path.isfile('./data/raw/' + boundVolume + '.pdf'):
            print('Skipping', boundVolume, '- File already exists')
            continue

        print('Downloading and Writing Bound Volume ', boundVolume, '....', end='')
        req = requests.get('https://www.supremecourt.gov/opinions/boundvolumes/' + boundVolume + 'bv.pdf')
        fi = open('./data/raw/' + boundVolume + '.pdf', 'wb')
        fi.write(req.content)
        fi.close()
        print('Done')

getData()