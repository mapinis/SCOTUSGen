from textgenrnn import textgenrnn

generator = textgenrnn()
generator.train_from_largetext_file('data/text/502.txt', new_model=True);

print(generator.generate_samples())