#!/usr/bin/env python3

import csv
import math
import matplotlib.pyplot as plt
import numpy as np
    
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

# This function returns the pre-compited values of exp_max
# since it takes a long time to compute
def exp_max_prec(X: list, mus: list, var: list, ITERATION: int):
    match len(mus):
        case 2:
            mus = [-3.07, 4.04]
            var = [7.63, 1.39]
            p_colours = [0.568, 0.432]
        case 3:
            mus = [-4.72, 0.410, 4.26]
            var = [3.07, 5.96, 0.980]
            p_colours = [0.345, 0.302, 0.353]
        case 4:
            mus = [-4.78, 0.923, -0.812, 4.26]
            var = [2.96, 5.08, 7.94, 0.979]
            p_colours = [0.319, 0.167, 0.162, 0.352]
        case _:
            mus, var, p_colours = exp_max_prec(measurements, mus, var, ITERATION)

    return(mus, var, p_colours)

def exp_max(X: list, mus: list, var: list, ITERATION: int):
    if len(mus) != len(var):
        return
    n: int = len(mus)
    prob_color = [1/n for c in range(n)]
    for _ in range(ITERATION):
        prob_colour_xi: list = [[] for c in range(n)]
        for x in X:
            prob_xi_colour: list = [
                norm_pdf(x, mu, var) * p_colour
                for mu, var, p_colour in zip(mus, var, prob_color)
            ]

            denominator: float = sum(prob_xi_colour)
            for c in range(n):
                prob_colour_xi[c].append(prob_xi_colour[c] / denominator)

        for c in range(n):
            prob_colour_fixed_x: list = prob_colour_xi[c] 
            denominator = sum(prob_colour_fixed_x)
            
            mus[c] = sum(
                x * prob
                for x, prob in zip(X, prob_colour_fixed_x)
            ) / denominator

            var[c] = sum(
                prob * (x - mus[c])**2
                for x, prob in zip(X, prob_colour_fixed_x)
            ) / denominator
            
            prob_color[c] = denominator / len(X)

    return(mus, var, prob_color)


def plot_exp_max(measurements: list, mus: list, variances: list, p_colours: list, ax):
    w = np.linspace(min(measurements), max(measurements), 1000)
    z = [
        sum(
            norm_pdf(x, mus[i], variances[i]) * p_colours[i]
            for i in range(len(mus))
        )
        for x in w
    ]
    ax.plot(w, z, label=f'Expectation maximization n={len(mus)}')
    ax.legend(loc=2, prop={'size': 10})
    return z


def point2(measurements: list, times: list, old_ax, new_ax):
    for rank in range(1, 7):
         trend: list = least_square(times, measurements, rank)
         w = np.linspace(0,2,100)
         z = [np.polyval(trend, i) for i in w]
         old_ax.plot(w, z, label = f"lstsqr - {rank}")
    
    old_ax.legend()
    old_ax.legend(loc=3, prop={'size': 10})

    trend: list = least_square(times, measurements, 5)
    for i in range(len(measurements)):
         measurements[i] = measurements[i] - np.polyval(trend, times[i])

    new_ax.scatter(times, measurements, label='De-trended scatterplot')
    new_ax.legend(loc=3, prop={'size': 10})

def point4(measurements: list, times: list, ax):
    ax.hist(measurements, bins=200, density=True, label='De-trended histogram')
    mus, variances, p_colours = exp_max_prec(measurements, [-5,0,5], [1, 1, 1], 900)
    plot_exp_max(measurements, mus, variances, p_colours, ax)

def point5(measurements: list, times: list, ax):
    ax.hist(measurements, bins=200, density=True, label='De-trended histogram')
    MIN_V = -10
    MAX_V = 10
    INTERVAL = 50
    STEP = (MAX_V - MIN_V) / INTERVAL
    n_i = [0 for _ in range(INTERVAL)]
    for measurement in measurements:
        i = min(INTERVAL - 1, max( math.floor((measurement - MIN_V) / (MAX_V - MIN_V) * INTERVAL), 0))
        n_i[i] += 1 

    cont = True
    old_T = float('inf')
    i = 2
    while(cont):
        start_mu = list(np.linspace(MIN_V, MAX_V, i + 1, endpoint=False))
        start_mu.pop(0)
        mus, variances, p_colours = exp_max_prec(measurements, start_mu, [1] * i, 500 * i)
        # print("Done ", i)
        # print(mus, variances, p_colours)
        plot_exp_max(measurements, mus, variances, p_colours, ax)
        p_i = [
            sum(
                norm_pdf(x + STEP / 2, mus[i], variances[i]) * p_colours[i]
                for i in range(len(mus))
            ) * ((MAX_V - MIN_V) / INTERVAL)
            for x in np.linspace(MIN_V, MAX_V, INTERVAL, endpoint = False)
        ]

        T = sum(
            (n_i[k] - len(measurements) * p_i[k])**2/ (len(measurements) * p_i[k])
            for k in range(INTERVAL)
        )
        print("T =",T, "with i=", i)
        
        cont = (old_T - T) / T > 0.10
        old_T = T
        i += 1

def main():
    csvFile = csv.reader(open('data_ex1_wt.csv', mode ='r'))
    measurements: list = []
    times: list = []
    for line in csvFile:
        times.append(float(line[0]))
        measurements.append(float(line[1]))
         
    # POINT 1
    fig1, ax1 = plt.subplots(1, 1)
    ax1.scatter(times, measurements, label='Scatterplot', color='grey')
    
    # POINT 2
    fig2, ax2 = plt.subplots(1, 1)
    point2(measurements, times, ax1, ax2)
    fig1.savefig('point1.png', bbox_inches='tight')
    fig2.savefig('point2.png', bbox_inches='tight')
    
    # POINT 3
    fig3, ax3 = plt.subplots(1, 1)
    ax3.hist(measurements, bins=200, density=True, label='De-trended histogram')
    fig3.savefig('point3.png', bbox_inches='tight')
    
    # POINT 4
    fig4, ax4 = plt.subplots(1, 1)
    point4(measurements, times, ax4)
    fig4.savefig('point4.png', bbox_inches='tight')

    # POINT 5
    fig5, ax5 = plt.subplots(1, 1)
    point5(measurements, times, ax5)
    fig5.savefig('point5.png', bbox_inches='tight')

    print("plots have been saved as images")
    
if __name__ == "__main__":
    main()
