# SCOTUSGen
Supreme Court Opinion Generator

Live at http://scotusgen.herokuapp.com/

(warning, will take a while, this is *not* efficient)

## Inspiration
As a last act of High School, I had to complete a May Term project. It could be anything I wanted it to be as long as it was academic or creative, and I chose to combine two of my great interests: computer science and constitutional law.

So I asked myself the question, can I write something that generates a fake Supreme Court opinion, based on previous ones?

The answer: Yes, kinda, but the sentences don't make sense and it's very slow, and sometimes it just doesn't work, especially when many people try to use the site at once. Ooops. But sometimes the results are funny!

## How It Works
There exists a Python library called textgenrnn, which is a neural-network based text generator built on TensorFlow. When the application runs, the generator creates about 7000 characters of text, which is then stripped and normalized. These 7000 characters are then rendered into a LaTeX template, which is used to generate a PDF which is fed to the user.

## The Model
The model for the neural network is included in the repository, and on startup the generator just uses this model. Creating this model, however, was a process.

As detailed in the setup folder and setup.py, the model is trained off of around 60 PDFs downloaded off the SCOTUS website, each of which contains many dozens of cases. Ghostscript is used to extract the text from these PDFs, and then these text files are fed into the neural network to train.

Feel free to train and use your own model, just be aware that it took over 48 hours of non-stop training on my i5 4690k overclocked to 4.5 GHz. Yes, it was kept cool the whole time. No, I do not pay the power bill. It will probably be faster with an Nvidia Card.

## What I learned

Combining many frameworks can be a pain, and shoving a LaTeX instance into Heroku is even more of a pain.

Nevertheless, I do consider the project a success, despite it's half-working and very ugly state. This was decided by my school to be a completed May Term project.
