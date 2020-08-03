import csv
import statistics
import matplotlib.pyplot as plt

linecount = 0
filename = input("file for analysis: ")
filename = filename + ".csv"

def VisualiseCSV():
    F0Values = []
    RMSEnergies = []
    LoudnessVals = []
    voicePresentValues = []
    frameNumbers = []
    global linecount
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if len(row) == 10: # check the row has finished writing from OpenSmile
                if linecount == 0:
                    print(f'Column names are {", ".join(row)}')
                    linecount += 1
                else:
                    frameNumber = float(row[0])
                    frameNumbers.append(frameNumber)
                    voicePresentLikelihood = float(row[2])
                    if voicePresentLikelihood < 0:
                        voicePresentLikelihood = 0
                    voicePresentValues.append(voicePresentLikelihood)
                    F0value = float(row[5])
                    F0Values.append(F0value)
                    RMSEnergy = float(row[3])
                    RMSEnergies.append(RMSEnergy)
                    loudness = float(row[9])
                    LoudnessVals.append(loudness)

    plt.figure(1)
    plt.plot(frameNumbers, F0Values)
    plt.figure(2)
    plt.plot(frameNumbers, RMSEnergies)
    plt.figure(3)
    plt.plot(frameNumbers, LoudnessVals)
    plt.figure(4)
    plt.plot(frameNumbers, voicePresentValues)
    plt.show()


VisualiseCSV()
