import csv
import statistics

oldFrameNumber = 0
frameNumber = 0
linecount = 0

def readInCSV():
    F0Values = []
    RMSEnergies = []
    LoudnessVals = []
    global linecount
    global frameNumber
    global oldFrameNumber
    with open('secondTestOfLive.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for i in range(oldFrameNumber):
            next(csv_reader)
        for row in csv_reader:
            if len(row) == 10: # check the row has finished writing from OpenSmile
                if linecount == 0:
                    print(f'Column names are {", ".join(row)}')
                    linecount += 1
                else:
                    voicePresentLikelihood = float(row[2])
                    if voicePresentLikelihood > 0: # Check if there is a voice present
                        F0value = float(row[5])
                        if F0value > 0:
                            F0Values.append(F0value)
                        RMSEnergy = float(row[3])
                        if RMSEnergy > 0:
                            RMSEnergies.append(RMSEnergy)
                        loudness = float(row[9])
                        if loudness > 0:
                            LoudnessVals.append(loudness)
                    frameNumber = int(row[0])
    averageF0 = statistics.mean(F0Values)
    stdF0 = statistics.stdev(F0Values)
    averageEnergy = statistics.mean(RMSEnergies)
    stdEnergy = statistics.stdev(RMSEnergies)
    averageLoud = statistics.mean(LoudnessVals)
    stdLoud = statistics.stdev(LoudnessVals)
    # Here we iterate backwards through the F0 values and discover if there was a upturn or down turn in pitch which
    # is greater than the 2 SD. If it is. Then we compute that occurrence's length from the end of the utterance, the
    # further from the end the less the probability that it marks the end of the turn
    F0endOfTurnProb = 0
    marker = 0
    LengthOfF0Data = len(F0Values)
    lowerBound = averageF0 - (2*stdF0)
    upperBound = averageF0 + (2*stdF0)
    for i in range(len(F0Values) - 1, -1, -1):
        if lowerBound > F0Values[i] or F0Values[i] > upperBound:
            marker = i
            break
    F0endOfTurnProb = marker/LengthOfF0Data*100

    # We then do the same for energy and loudness
    EnergyendOfTurnProb = 0
    marker = 0
    LengthOfEnergyData = len(RMSEnergies)
    lowerBound = averageEnergy - (2*stdEnergy)
    upperBound = averageEnergy + (2*stdEnergy)
    for i in range(len(F0Values) - 1, -1, -1):
        if lowerBound > RMSEnergies[i] or RMSEnergies[i] > upperBound:
            marker = i
            break
    EnergyendOfTurnProb = marker/LengthOfEnergyData*100

    LoudnessEndOfTurnProb = 0
    marker = 0
    LengthOfLoudnessData = len(LoudnessVals)
    lowerBound = averageLoud - (2 * stdLoud)
    upperBound = averageLoud + (2 * stdLoud)
    for i in range(len(LoudnessVals) - 1, -1, -1):
        if lowerBound > LoudnessVals[i] or LoudnessVals[i] > upperBound:
            marker = i
            break
    LoudnessEndOfTurnProb = marker / LengthOfLoudnessData * 100

    return F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb

whileLoop = True

while whileLoop:
    keypress = input()
    if keypress == "t":
        oldFrameNumber = frameNumber        
        F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb = readInCSV()
        keypress = "r"
        
        print(F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb)
        print("read")
    if keypress == "y":
        whileLoop = False

print(frameNumber)
