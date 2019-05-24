from textgenrnn import textgenrnn
import os


def generateModel():
    generator = textgenrnn(name="model")

    files = os.listdir("data/text")

    print("Training on", files[0])
    generator.train_from_largetext_file(
        "data/text/" + files[0],
        new_model=True,
        num_epochs=2,
        batch_size=256,
        validate=False,
        dropout=20,
    )

    for fileName in files[1:]:
        print("Training on", fileName)
        generator.train_from_largetext_file(
            "data/text/" + fileName,
            new_model=False,
            num_epochs=2,
            batch_size=256,
            validate=False,
            dropout=20,
        )

    generator.save("../model/model_weights.hdf5")

