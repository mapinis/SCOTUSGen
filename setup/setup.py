import os

from getData import getData
from getText import getText
from generateModel import generateModel

print("Setting Up...")
newDownloads = getData()
getTextOut = getText()

print("\nDone downloading and converting.")
print("Summary:")
print("\tDownloaded Files:", newDownloads)
print("\tSuccessfully Converted Files:", getTextOut["converted"])
print("\tBad Files:", getTextOut["badFiles"])

if os.path.isfile("model.hdf5"):
    print("\nModel already generated, skipping.")
else:
    inp = input(
        "Generate Model? (WARNING: Will take a LONG time, possibly DAYS) (Y/N): "
    )
    while inp != "Y" and inp != "N":
        inp = input(
            "Generate Model? (WARNING: Will take a LONG time, possibly DAYS) (Y/N): "
        )
    if inp == "Y":
        print("It's your funeral...")
        generateModel()

print("\nDone")
