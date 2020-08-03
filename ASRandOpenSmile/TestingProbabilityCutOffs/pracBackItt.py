import csv
import statistics
import matplotlib.pyplot as plt


array = [1,2,3,4,5,6,7,8,9,10]

markers = []
for i in range(len(array) - 3, -1, -1):
    markers.append(i)
    print(markers)

