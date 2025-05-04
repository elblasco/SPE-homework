#!/usr/bin/env python3

import csv
import math
import matplotlib.pyplot as plt
import numpy as np

def point1(measurements: list, times: list, ax):
    ax[0].scatter(times, measurements, label='Scatterplot', color='grey')

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
    for _ in range(300):
        prob_colour_xi: list = [[] for c in range(n)]
        for i in range(len(X)):
            prob_xi_colour: list = []
            for c in range(n):
                prob_xi_colour.append(norm_pdf(X[i], mus[c], var[c]))

            denominator: float = sum(
                prob_xi_colour[c] * prob_color[c] for c in range(n)
            )
            
            for c in range(n):
                prob_colour_xi[c].append(prob_xi_colour[c] * prob_color[c] / denominator)

        for c in range(n):
            denominator = sum(
                prob_colour_xi[c][i]
                for i in range(len(X))
            )
            
            mus[c] = sum(
                prob_colour_xi[c][i] * X[i]
                for i in range(len(X))
            ) / denominator

            var[c] = sum(
                prob_colour_xi[c][i] * (X[i] - mus[c])**2
                for i in range(len(X))
            ) / denominator
            
            prob_color[c] = denominator / len(X)

    return(mus, var, prob_color)


def main():
    csvFile = csv.reader(open('data_ex1_wt.csv', mode ='r'))
    measurements: list = []
    times: list = []
    for line in csvFile:
        times.append(float(line[0]))
        measurements.append(float(line[1]))
    fig, ax = plt.subplots(1, 2)
    plt.xticks(size = 22)
    plt.yticks(size = 22)
    point1(measurements, times, ax)

    for rank in range(1, 7):
         trend: list = least_square(times, measurements, rank)
         w = np.linspace(0,2,100)
         z = [np.polyval(trend, i) for i in w]
         ax[0].plot(w, z, label = f"lstsqr - {rank}")
    
    ax[0].legend()
    ax[0].legend(loc=3, prop={'size': 14})
    trend: list = least_square(times, measurements, 5)
    for i in range(len(measurements)):
         measurements[i] = measurements[i] - np.polyval(trend, times[i])
    ax[1].scatter(times, measurements, label='De-trended scatterplot')
    ax[1].legend(loc=3, prop={'size': 14})
    # #mus, variances, p_colours = exp_max(measurements, [-1,0,1], [1, 1, 1])
    # mus = [-4.72, 0.41, 4.26]
    # variances = [3.07, 5.96, 0.98]
    # p_colours = [0.345, 0.302, 0.353]
    
    # ax[1].hist(measurements, bins=200, density=True)
    # w = np.linspace(min(measurements), max(measurements), 1000)
    # z = [
    #     sum(
    #         norm_pdf(x, mus[i], variances[i]) * p_colours[i]
    #         for i in range(len(mus))
    #     )
    #     for x in w
    # ]
    # ax[1].plot(w, z)
    plt.show()

    
    
    
if __name__ == "__main__":
    main()
