import os
import subprocess

if not os.path.isdir('data/text'):
        os.mkdir('data/text')

#for fileName in os.listdir('./data/raw'):
fileName="502.pdf"
fileName = fileName[:-4]

subprocess.run(['gswin64c -sDEVICE=txtwrite -o ./data/text/' + fileName + '.txt ./data/raw/' + fileName + '.pdf'], shell=True)

print(f'Starting trimming for {fileName}')
fi = open(f'data/text/{fileName}.txt', 'a+')
text = fi.read()
start = text.replace('CASESADJUDGED', '', 1).find('CASESADJUDGED') + 13
stop = text.find('ORDERS FOR')
fi.seek(0)
fi.write(text[start:stop])
fi.truncate()
fi.close()

