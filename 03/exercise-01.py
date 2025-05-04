#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import numpy as np

def point1(measurements: list, times: list):
    fig, ax = plt.subplots()
    ax.scatter(times, measurements)
    plt.show()

def sqrt(times: list, measurements: list, m: int):
    y: list = measurements
    x: list = times
    A: list = []
    
    for entry in x:
        A.append([entry**i for i in range(m+1)])

    AT: list = np.transpose(A)

    inv_mul= np.linalg.inv(np.matmul(AT, A))

    b: list = np.matmul(np.matmul(inv_mul, AT), y)
    
    w = np.linspace(0,10,100)
    z = [np.polyval(np.flip(b), i) for i in w]
    fig, ax = plt.subplots()
    ax.plot(w,z)
    plt.show()
    print(b)
    
def main():
    csvFile = csv.reader(open('data_ex1_wt.csv', mode ='r'))
    measurements: list = []
    times: list = []
    for line in csvFile:
        times.append(float(line[0]))
        measurements.append(float(line[1]))

    #point1(measurements, times)

    #for i in range(10):
    sqrt(times, measurements, 6)

    #w.r.t. Slides y = measurements and x = times

    
if __name__ == "__main__":
    main()
