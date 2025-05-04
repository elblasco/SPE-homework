#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt

def main():
    csvFile = csv.reader(open('data_ex1_wt.csv', mode ='r'))
    measurements: list = []
    times: list = []
    for line in csvFile:
        times.append(line[0])
        measurements.append(line[1])

    fig, ax = plt.subplots()
    ax.scatter(times, measurements)
    plt.show()
    
if __name__ == "__main__":
    main()
