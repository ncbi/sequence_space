#! /usr/bin/env python3

import sys, math

def sigmoid(x):

    return 1.0/(1.0+math.exp(-x))

if __name__ == '__main__':

    f = open(sys.argv[1]).read().splitlines()

    for i in range(2,len(f)):

        info = f[i].split()

        if not info:
            continue

        try:
            n = int(info[0])
        except ValueError:
            continue

        line = []
            
        for j in info[2:22]:

                line.append(sigmoid(int(j)))

        print('%1.8f '*20 %tuple(line))
        #print line[-1]
