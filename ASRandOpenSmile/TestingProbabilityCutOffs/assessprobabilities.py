import csv
import statistics
import matplotlib.pyplot as plt


def assessThisFile(filename, filenameOfMarkers):
    turns = []
    frames = []
    linecount = 0
    with open(filenameOfMarkers) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if linecount == 0:
                linecount += 1
            else:
                data = []
                startOfTurn = float(row[0])
                endOfTurn = float(row[1])
                data.append(startOfTurn)
                data.append(endOfTurn)
                turns.append(data)

    linecount = 0
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if linecount == 0:
                linecount += 1
            else:
                data = []
                frameNumber = float(row[0])
                data.append(frameNumber)
                frameTime = float(row[1])
                data.append(frameTime)
                voicePresentLikelihood = float(row[2])
                data.append(voicePresentLikelihood)
                F0value = float(row[5])
                data.append(F0value)
                RMSEnergy = float(row[3])
                data.append(RMSEnergy)
                loudness = float(row[9])
                data.append(loudness)
                frames.append(data)

    def VisualiseCSV(startTurnSeconds, EndTurnSeconds):
        F0Values = []
        RMSEnergies = []
        LoudnessVals = []
        # Find the start frame index and end frame index
        for x in frames:
            if x[1] > startTurnSeconds and x[1] < EndTurnSeconds + 1:
                if x[3] > 0: #if a voice is present
                    F0value = x[3]
                    if F0value > 0:
                        F0Values.append(F0value)
                    RMSEnergy = x[4]
                    if RMSEnergy > 0:
                        RMSEnergies.append(RMSEnergy)
                    loudness = x[5]
                    if loudness > 0:
                        LoudnessVals.append(loudness)

        averageF0 = statistics.mean(F0Values)
        stdF0 = statistics.stdev(F0Values)
        averageEnergy = statistics.mean(RMSEnergies)
        stdEnergy = statistics.stdev(RMSEnergies)
        averageLoud = statistics.mean(LoudnessVals)
        stdLoud = statistics.stdev(LoudnessVals)

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
        marker = 0
        LengthOfEnergyData = len(RMSEnergies)
        lowerBound = averageEnergy - (2 * stdEnergy)
        upperBound = averageEnergy + (2 * stdEnergy)
        for i in range(len(RMSEnergies) - 1, -1, -1):
            if lowerBound > RMSEnergies[i] or RMSEnergies[i] > upperBound:
                marker = i
                break
        EnergyendOfTurnProb = marker / LengthOfEnergyData * 100

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


    F0eachTurn = []
    EnergyPerTurn = []
    LoudnessPerTurn = []

    for x in turns:
        data = []
        F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb = VisualiseCSV(x[0], x[1])
        if F0endOfTurnProb > 0:
            F0eachTurn.append(F0endOfTurnProb)
        if EnergyendOfTurnProb > 0:
            EnergyPerTurn.append(EnergyendOfTurnProb)
        if LoudnessEndOfTurnProb > 0:
            LoudnessPerTurn.append(LoudnessEndOfTurnProb)

    averageF0 = statistics.mean(F0eachTurn)
    stdF0 = statistics.stdev(F0eachTurn)
    averageEnergy = statistics.mean(EnergyPerTurn)
    stdEnergy = statistics.stdev(EnergyPerTurn)
    averageLoud = statistics.mean(LoudnessPerTurn)
    stdLoud = statistics.stdev(LoudnessPerTurn)

    return averageF0, averageEnergy, averageLoud


averageF0, averageEnergy, averageLoud = assessThisFile("17yearoldgirlsconversation.csv", "handMarkedEOTforFemaleConvo.csv")
print(averageF0, averageEnergy, averageLoud)
averageF0, averageEnergy, averageLoud = assessThisFile("18yearoldboysconversation.csv", "handMarkedEOTforMaleConvo.csv")
print(averageF0, averageEnergy, averageLoud)