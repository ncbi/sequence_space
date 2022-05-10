#! /usr/bin/env python3

from Bio import SeqIO
import sys

records = SeqIO.parse(sys.argv[1], "fasta")
count = SeqIO.write(records, sys.argv[2], "stockholm")
print("Converted %i records" % count)
