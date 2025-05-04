#!/usr/bin/env python3

import csv
import math
import matplotlib.pyplot as plt
import numpy as np

def point1(measurements: list, times: list, ax):
    ax.scatter(times, measurements)

def least_square(times: list, measurements: list, m: int):
    y: list = measurements
    x: list = times
    A: list = []
    
    for entry in x:
        A.append([entry**i for i in range(m+1)])

    AT: list = np.transpose(A)

    inv_mul= np.linalg.inv(np.matmul(AT, A))

    b: list = np.matmul(np.matmul(inv_mul, AT), y)

    return(np.flip(b))

def norm_pdf(x, mu, var):
    return (1/(math.sqrt(2 * math.pi * var))) * math.exp(- (((x-mu)**2)/(2 * var)))

def exp_max(X: list, mus: list, var: list):
    if len(mus) != len(var):
        return
    n: int = len(mus)
    prob_color = [1/n for c in range(n)]
    for _ in range(1000):
        prob_colour_xi: list = [[] for c in range(n)]
        for i in range(len(X)):
            prob_xi_colour: list = []
            for c in range(n):
                prob_xi_colour.append(norm_pdf(X[i], mus[c], var[c]))
            denominator: float = 0
            for c in range(n):
                denominator += (prob_xi_colour[c] * prob_color[c])
            for c in range(n):
                prob_colour_xi[c].append(prob_xi_colour[c] * prob_color[c] / denominator)

        for c in range(n):
            denominator = 0
            for i in range(len(X)):
                denominator += prob_colour_xi[c][i]
            mus[c] = 0
            for i in range(len(X)):
                mus[c] += prob_colour_xi[c][i] * X[i] / denominator

            var[c] = 0
            for i in range(len(X)):
                var[c] += prob_colour_xi[c][i] * (X[i] - mus[c])**2 / denominator
            prob_color[c] = denominator / len(X)

    print(mus, var)
def main():
    csvFile = csv.reader(open('data_ex1_wt.csv', mode ='r'))
    measurements: list = []
    times: list = []
    for line in csvFile:
        times.append(float(line[0]))
        measurements.append(float(line[1]))

    # fig, ax = plt.subplots()
    
    # point1(measurements, times, ax)
    # for i in range(10):
    #     trend: list = least_square(times, measurements, i)
    #     w = np.linspace(0,2,100)
    #     z = [np.polyval(trend, i) for i in w]
    #     ax.plot(w, z)

    # plt.show()
    trend: list = least_square(times, measurements, 5)
    for i in range(len(measurements)):
        measurements[i] = measurements[i] - np.polyval(trend, times[i])

    #fig, ax = plt.subplots()
    #ax.scatter(times, measurements)
    #ax.ecdf(measurements)
    #ax.hist(measurements, bins=200, density=True)
    #plt.show()

    exp_max(measurements, [-1,0,1], [1, 1, 1])
    
    
    
if __name__ == "__main__":
    main()
