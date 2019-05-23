import os
import requests

# Downloads all bound volumes off Supreme Court website
def getData():
    # Create file structure
    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isdir("data/raw"):
        os.mkdir("data/raw")

    boundVolumesRange = map(str, range(502, 570))  # Start 502, Stop 570 for all volumes

    newDownloads = []
    for boundVolume in boundVolumesRange:

        # Save time by making sure not already downloaded
        if os.path.isfile("./data/raw/" + boundVolume + ".pdf"):
            print("Skipping Downloading", boundVolume, "- File already exists")
            continue

        # Download
        print(
            "Downloading and Writing Bound Volume",
            boundVolume,
            "....",
            end="",
            flush=True,
        )
        req = requests.get(
            "https://www.supremecourt.gov/opinions/boundvolumes/"
            + boundVolume
            + "bv.pdf"
        )
        fi = open("./data/raw/" + boundVolume + ".pdf", "wb")
        fi.write(req.content)  # write to new file
        fi.close()
        print("Done", flush=True)
        newDownloads.append(boundVolume + ".pdf")

    return newDownloads
