#! /usr/local/bin/python3.8

import sys, string
import numpy as np
from matplotlib import pyplot as plt

def get_data(f):

    identities = []

    for i in range(1,len(f)):

        info = f[i].split(',')

        for j in range(2,len(f)):

            if info[j] == '':
                continue

            identities.append(float(info[j]))

    return np.array(identities)
    

if __name__ == '__main__':

    f = open('RfaH_identity_matrix.txt').read().splitlines()
    f2 = open('NFS_SIM.txt').read().splitlines()

    identities1 = get_data(f)
    identities2 = get_data(f2)

    fig, ax = plt.subplots(figsize=(3.5,6))

    boxInfo = ax.violinplot([identities1,identities2],[1,1.6],points=41,showextrema=False)

    boxInfo['bodies'][0].set_facecolor('#00AAAA')
    boxInfo['bodies'][0].set_alpha(1)
    boxInfo['bodies'][1].set_facecolor('#C74B40')
    boxInfo['bodies'][1].set_alpha(1)

    ax.set_xticks([1,1.6])
    ax.set_xticklabels(['Fold\nSwitch','Single\nFold'],size=12)
    ax.set_ylabel('Pairwise sequence identity (%)',size=12)
    plt.title('Sequence identity distributions \nof all predictions',size=12)
    fig.tight_layout(pad=1)

    plt.savefig(sys.argv[1]+'.png',dpi=300)
