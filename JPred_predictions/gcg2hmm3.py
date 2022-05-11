#! /usr/bin/env python3

import sys, math

def sigmoid(x):

    return 1.0/(1.0+math.exp(-x/100.0))

if __name__ == '__main__':

    f = open(sys.argv[1]).read().splitlines()

    for i in range(11,len(f)):

        info = f[i].split()

        if len(info) == 27:

            line = []
            
            for j in info[1:-2]:

                line.append(sigmoid(int(j)))

            print('%1.5f '*23 %tuple(line[:-1])+'%1.5f' %(line[-1]))
