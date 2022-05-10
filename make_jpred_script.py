#! /usr/bin/env python3

import sys

if __name__ == '__main__':

    print("#! /bin/bash")
    print('')

    f = open(sys.argv[1]).read().splitlines()

    for i in f:

        ID = i.split('/')[-1].strip()

        print('./jpred_pipeline_updated.sh %s' %(i.strip()+'/'+ID))
