import os
import subprocess

# Takes files with provided names from data/raw (or all files if left blanck) and extracts text from them, using ghostscript
# Trims each text file such that only opinions are included
# ghostscript occasionally fails on certain files, reason unknown, cutting out the majority of pages
# script detects these failures and deletes the text file if it is a bad failure (gs cuts out all opinion pages)
# lets it pass if ok (gs cuts out initial cases, but not all)
# returns the names of converted, failed, and ok files
def getText(files=None):
    if files == None:
        files = os.listdir("data/raw")

    if not os.path.isdir("data/text"):
        os.mkdir("data/text")

    # After one run, the list of bad files will be saved, so it cna be skipped with next setup run
    if os.path.isfile("badFiles.txt"):
        badFilesHolder = open("badFiles.txt", "r")
        badFiles = [line.strip('\n') for line in badFilesHolder.readlines()]
        badFilesHolder.close()
    else:
        badFiles = []

    noAdjudged = []
    converted = []

    for fileName in files:
        fileName = fileName[:-4]

        # Saves time by checking if file already converted
        if os.path.isfile("./data/text/" + fileName + ".txt"):
            print("Skipping Converting", fileName, "- Text already extracted")
            continue
        if fileName in badFiles:
            print("Skipping Converting", fileName, "- Known Bad File")
            continue

        # Run ghostscript
        print("Converting", fileName, "...", end="", flush=True)
        subprocess.run(
            [
                "gs",
                "-sDEVICE=txtwrite",
                "-q",
                "-o",
                "data/text/" + fileName + ".txt",
                "data/raw/" + fileName + ".pdf",
            ]
        )
        print("Done", flush=True)

        print("Trimming", fileName)
        fi = open("data/text/" + fileName + ".txt", "r", errors="ignore")
        text = fi.readlines()

        checkStr = text[1].strip("\t \n")
        # If either of these are in this string, first page converted is an index or orders page, not opinion page
        if "INDEX" in checkStr or "ORDERS" in checkStr:
            print("BAD FILE:", fileName)
            fi.close()
            subprocess.run(["rm", "data/text/" + fileName + ".txt"])  # delete the file
            badFiles.append(fileName)
            continue  # move on

        # Find where the opinions begin and end
        start = -1
        stop = len(text)

        for i in range(len(text)):
            checkStr = text[i].replace(" ", "").replace(" ", "").strip("  \n\t")
            if "ADJUDGED" in checkStr:  # Finds last instance of "ADJUDGED"
                start = i
            if "ORDERSFOR" in checkStr and i < stop:
                # Finds first instance of "ORDERSFOR"
                stop = i
        if (
            start < 0
        ):  # No start found, meaning gs failed, but wasn't caught earlier meaning it is an ok failure
            noAdjudged.append(fileName)
        if stop < 0:  # No stop found, which is very bad
            raise Exception("ORDERSFOR not found in " + fileName)

        # Make the text (one line, from start to stop)
        text = " ".join(
            list(map(lambda line: line.strip("\t \n"), text[start + 1 : stop]))
        )

        fi.close()
        fi = open("data/text/" + fileName + ".txt", "w")
        fi.write(text)
        fi.close()

        converted.append(fileName)

    badFilesHolder = open("badFiles.txt", "w")
    badFilesHolder.writelines([badFile + "\n" for badFile in badFiles])
    badFilesHolder.close()

    return {"converted": converted, "badFiles": badFiles, "noAdjudged": noAdjudged}
