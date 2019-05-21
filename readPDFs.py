import PyPDF2
import os
import wordninja

#for fileName in os.listdir('./data'):
fi = open('data/raw/502.pdf', 'rb')
boundVolume = PyPDF2.PdfFileReader(fi)

for i in range(boundVolume.getNumPages()):
    page = boundVolume.getPage(i)
    text = page.extractText()
    lines = list(filter(lambda x: x != '', text.replace('ª', '“').replace('º', '”').replace('®', 'fi').replace('Ð', '—').replace('±', '–').split('\n')))

    outLines = []
    started = False
    for line in lines:
        if started:
            outLines.append(line.strip('-'))
        if line == 'OpinionoftheCourt' or line[-10:] == 'dissenting' or line[-20:] == 'concurringinjudgment':
            started = True

#print(' '.join(wordninja.split(''.join(outLines))))

# https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
