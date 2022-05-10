#! /usr/bin/env python3

import sys
import numpy as np
from matplotlib import pyplot as plt
import pickle
import pandas as pd
from Bio import pairwise2
import os

ref1 = '---EEEEEEEE----EEEEEEEE------EEEEEEEEE--'
ref2 = '---EEEEEEE-----EEEEEEEEE-----EEEEE------'

ref_seqs = {'RfaH_CTDs':'FEGFQAIFTEPDGEARSMLLLNLINKEIKHSVKNTEFRKL',
            'NusG_CTDs':'ADFNGVVEEVDYEKSRLKVSVSIFGRATPVELDFSQVEKA'}

dir_dict = {'CTDs_40_jpred':'CTDs_40_uniprot90','full_seqs_jpred':'full_seqs_uniprot90'}
annotations = 'NusG_annotations_1119.txt'

def make_hist(dist,step):

    x_ax = [step*x for x in range(int(1.0/step) + 1)]

    hist = [0]*(int(1.0/step)+1)

    for i in dist:
        
        hist[int(i/step)] += 1


    return hist, x_ax

def update_pred_alignment(a,ref1,ref2,jpred1,jpred2):

    j1A = ''
    j2A = ''
    r1A = ''
    r2A = ''

    j = 0
    k = 0
    
    for i in range(len(a[0])):

        if a[0][i] == '-':
            j1A += '-'
            j2A += '-'

        else:
            j1A += jpred1[j]
            j2A += jpred2[j]
            j += 1

        if a[1][i] == '-':
            r1A += '-'
            r2A += '-'
        else:
            r1A += ref1[k]
            r2A += ref2[k]
            k += 1

    return r1A, r2A, j1A, j2A

def get_nseqs(dir,ID):
    
    nseq1 = 0

    if os.path.isfile(dir+'/'+ID+'/'+ID+'.forhmmer'):
        nseq1 = len(open(dir+'/'+ID+'/'+ID+'.forhmmer').read().splitlines())/2
    else:
        nseq1 = 1

    return nseq1

def get_annotation(info,idx):

    annotation = ''

    while idx < len(info) and '=' not in info[idx]:

        annotation += info[idx]+' '
        idx += 1

    return annotation[:-1], idx
        
def get_tax(info,idx):

    Tax = ''

    for i in range(idx,len(info)):
        if 'Tax=' in info[i]:
            Tax += info[i][4:]+' '
            if i+1 == len(info):
                return Tax[:-1]

            if 'RepID' not in info[i+1]:
                Tax += info[i+1]
                return Tax

    return Tax

def parse_annotations(annotations, IDs):

    a = open(annotations).read().splitlines()

    annotation_list = []
    tax = []

    aDict = {}
    annotation = ''
    Tax = ''

    for i in a:

        info = i.split()
        ID = info[1].split('_')[-1]
        annotation,idx = get_annotation(info,2)
        Tax = get_tax(info,idx)
        if ID in aDict:
            if len(annotation) > len(aDict[ID][0]):
                aDict[ID][0] = annotation
            if len(Tax) > len(aDict[ID][1]):
                aDict[ID][1] = Tax
        else:
            aDict[ID] = [annotation,Tax]


    for ID in IDs:

        if ID in aDict:
            annotation_list.append(aDict[ID][0])
            tax.append(aDict[ID][1])
        else:
            annotation_list.append('')
            tax.append('')

    return tax, annotation_list
        
if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit('Usage: ./collage_preds.py <input list of sequences> <output filename without extension>')

    f = open(sys.argv[1]).read().splitlines()
    f2 = open("code2node.pkl","rb")

    RIs =open('RfaH_IDs.txt').read().splitlines()

    RfaH_IDs = [x.strip() for x in RIs]

    codes = pickle.load(f2)
    preds = [-999]*305
    apreds = {}

    j = 0

    step = 0.05

    pAtoB1 = []
    pAtoB2 = []
    IDs = []
    seqs = []
    spreds1 = []
    spreds2 = []
    conf1 = []
    conf2 = []
    
    overall_pred = []

    tpreds = []
    preds_used = []

    good_preds = []

    nseqs1A = []
    nseqs2A = []

    n = []

    cluster = []

    for i in f:

        ID = i.split('/')[-1]
        dir = '/'.join(i.split('/')[:-1])
        cdir = i.split('/')[-2]
        pwd = '/'.join(i.split('/')[:-2])

        IDs.append(ID)
        cluster.append(codes[ID])

        try:
            seq = open(i+'/'+ID+'.fa').read().splitlines()
            pred1 = open(i+'/'+ID+'.jnet').read().splitlines()
            pred2 = open(pwd+'/'+dir_dict[cdir]+'/'+ID+'/'+ID+'.jnet').read().splitlines()
            if ID in RfaH_IDs:
                ref_seq = ref_seqs['RfaH_CTDs']
            else:
                ref_seq = ref_seqs['NusG_CTDs']
        except:
            print('Could not open %s' %(pwd+'/'+dir_dict[cdir]+'/'+ID+'/'+ID+'.jnet'))
            continue

        seqs.append(seq[1])

        if len(pred1) < 7 or len(pred2) < 7:
            print(i)
            continue

        jpred1 = ''.join([x for x in pred1[1][9:] if x != ','])
        jpred2 = ''.join([x for x in pred2[1][9:] if x != ','])

        spreds1.append(jpred1)
        spreds2.append(jpred2)

        a = pairwise2.align.localxs(seq[1],ref_seq,-2.0,-0.5)

        refp1, refp2, jpred1, jpred2 = update_pred_alignment(a[0],ref1, ref2,
                                                           jpred1,jpred2)

        nseqs1 = get_nseqs(dir, ID)
        nseqs2 = get_nseqs(pwd+'/'+dir_dict[cdir],ID)
        
        nseqs1A.append(nseqs1)
        nseqs2A.append(nseqs2)

        if nseqs1 < 5 and nseqs2 < 5:
            conf1.append('Low confidence')
            conf2.append('Low confidence')
            pAtoB1.append('None')
            pAtoB2.append('None')
            tpreds.append('None')
            preds_used.append(0)
            overall_pred.append('None')
            print('Low confidence: %s' %(ID))
            continue

        refpred1 = ref1
        refpred2 = ref2

        atobdisc1 = len([x for x in range(len(jpred1)) if jpred1[x] == 'H' and \
                         refp1[x] == 'E'])
        atobdisc2 = len([x for x in range(len(jpred2)) if jpred2[x] == 'H' and \
                         refp2[x] == 'E'])

        norm1 = float(min(len([x for x in jpred1 if x in ['H','E']]),
                          len([x for x in refp1 if x in ['H','E']])))

        norm2 = float(min(len([x for x in jpred2 if x in ['H','E']]),
                          len([x for x in refp2 if x in ['H','E']])))

        if norm1 == 0:
            print('No SS Pred1 %i %s' %(i, jpred))
            continue

        if norm2 == 0:
            print('No SS Pred2 %i %s' %(i, jpred))
            continue


        percent_atob1 = atobdisc1/norm1
        percent_atob2 = atobdisc2/norm2

        if nseqs1 < 5 and nseqs2 >= 5:
            conf1.append('Low confidence')
            conf2.append('Good confidence')
            pAtoB1.append('None')
            pAtoB2.append(percent_atob2)
            preds_used.append(2)
            percent_atob = percent_atob2
            good_preds.append(1)

        elif nseqs1 >=5 and nseqs2 < 5:
            print('Weird result %s' %(ID))
            conf2.append('Low confidence')
            conf1.append('Good confidence')
            pAtoB2.append('None')
            pAtoB1.append(percent_atob1)
            preds_used.append(1)
            percent_atob = percent_atob1
            good_preds.append(1)
            
        else:
            percent_atob = np.mean([percent_atob1,percent_atob2])
            preds_used.append(3)
            conf2.append('Good confidence')
            conf1.append('Good confidence')
            pAtoB2.append(percent_atob2)
            pAtoB1.append(percent_atob1)
            good_preds.append(1)

        tpreds.append(percent_atob)


        if preds[codes[ID]] == -999:
            preds[codes[ID]] = []

        if percent_atob >0.05:
            preds[codes[ID]].append(1)
            overall_pred.append('FS')
        else:
            preds[codes[ID]].append(0)
            overall_pred.append('NFS')

    scale = [-999]*305

    idxs = []

    for ID in IDs:

        if codes[ID] not in idxs:
            idxs.append(codes[ID])

    for i in idxs:

        scale[i] = np.mean(preds[i])

    print('Total NFS: %i' %(len([x for x in tpreds if x < 0.05])))
    print('Total Preds: %i' %(len(good_preds)))
    print('Total Seqs: %i' %(len(tpreds)))

    of = open('node_color_scale.pkl','wb')
    of.write(pickle.dumps(scale))

    of.close()

    tax, annotations = parse_annotations(annotations, IDs)

    d = {'Uniprot ID':IDs, 'Cluster ID': cluster, 'Annotation': annotations,\
         'Taxonomy': tax, 'CTD Seq':seqs, \
         'Overall Pred': overall_pred, 'Overall AtoB Disc': tpreds,\
         'Preds used': preds_used, 'Pred1':spreds1, \
         'Confidence 1':conf1, 'Pred2':spreds2, \
         'Confidence 2':conf2}

    df = pd.DataFrame(d)

    df = df[['Uniprot ID', 'Cluster ID', 'Annotation', 'Taxonomy', 'CTD Seq', \
             'Overall Pred', \
             'Overall AtoB Disc','Preds used', 'Pred1',\
             'Confidence 1', 'Pred2', 'Confidence 2']]

    df.to_csv(sys.argv[2]+'.csv')
