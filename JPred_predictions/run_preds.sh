#! /bin/bash

#Delete files from previous runs
rm all_seqs.txt
rm run_jpred.sh

#List absolute paths of all sequences in directories
for i in CTDs_40_jpred CTDs_40_uniprot90
do
    ls -d $PWD/${i}/* >> all_seqs.txt
done

#Make a script to run the JPred pipeline on all sequences in all directories
./make_jpred_script.py all_seqs.txt > run_jpred.sh
chmod u+x run_jpred.sh

#Run Jpred on Sequences
./run_jpred.sh

#Compare JPred predictions with NusG reference and collate
./collate_preds_final.py CTDs_40_jpred_sub.txt variants10


