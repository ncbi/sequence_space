#! /usr/bin/env python3

import sys
from Bio import pairwise2

def realign_seq(seq,insertion_indices,tlen):

    offset = 0
    s = ''
    i = 0

    while i < tlen:
        if i not in insertion_indices:
            s += seq[i-offset]
        else:
            s+= '-'
            offset += 1

        i += 1

    return s


def get_seqs(f):

    i = 0

    seq_start = 0
    seqs = []
    s = ''
    while i < len(f):

        if f[i][0] == '>':
            if i > 0 :
                seqs.append(s)
            s = ''

        else:
            s += f[i]
            
        i += 1

    return seqs
            
        
if __name__ == '__main__':

    f = open(sys.argv[1]).read().splitlines()

    seqs = get_seqs(f)

    if len(seqs[0]) > len(seqs[1]):

        a = pairwise2.align.localxs(seqs[0],seqs[1],-1.0,-0.5)
        insertion_indices = []

        for i in xrange(len(a[0][1])):
            if i < len(seqs[1]) and a[0][1][i] == '-' and seqs[1][i] !='-':
                insertion_indices.append(i)
            elif i >= len(seqs[1]):
                insertion_indices.append(i)

        for i in xrange(2,len(seqs)):
            s = realign_seq(seqs[i],insertion_indices,len(seqs[0]))
            print(s)

    else:
        for i in f:
            print(i)
        
