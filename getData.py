import os
import requests

def getData():
    if not os.path.isdir('data'):
        os.mkdir('data')

    boundVolumesRange = map(str, range(502, 510)) # Start 502, Stop 570 for all volumes
    
    for boundVolume in boundVolumesRange:
        print(f'Downloading and Writing Bound Volume {boundVolume}....', end='')
        req = requests.get('https://www.supremecourt.gov/opinions/boundvolumes/' + boundVolume + 'bv.pdf')
        fi = open('./data/' + boundVolume + '.pdf', 'wb')
        fi.write(req.content)
        fi.close()
        print('Done')

getData()