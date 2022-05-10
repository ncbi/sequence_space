#! /bin/bash

WDIR="/Users/porterll/data/sequence_space/code"

cat ${1}.fa > ${1}.bla7.f

F=${1}.pssm

#If sequences were hit in PSI-BLAST search and an MSA was generated
if test -f "$F"
    then
       cp ${1}.fa ${1}.bla7.fa
       #Make MSA out of PSI-BLAST sequences
       echo "Generating MSA from PSI-BLAST with mview"
       $WDIR/mview -out fasta ${1}.bla7 >> ${1}.bla7.fa
       #Format MSA for hmmer
       echo "Preparing MSA for hmmer"
       $WDIR/fix_MSA.py ${1}.bla7.fa > ${1}.forhmmer
       $WDIR/fasta2stockholm.py ${1}.forhmmer ${1}.stockholm
       #Get rid of old files if present
       rm ${1}.hmm
       rm ${1}.prf
       #Build HMM of MSA using hmmer and convert to JPred-recognized format
       echo "Running hmmer"
       $WDIR/hmmer-2.3.2/src/hmmbuild --fast --gapmax 1.0 --wblosum ${1}.hmm ${1}.stockholm
       $WDIR/hmmer-2.3.2/src/hmmconvert -p ${1}.hmm ${1}.prf
       $WDIR/gcg2hmm3.py ${1}.prf > ${1}.hmmat

       echo "Converting PSSM"
       $WDIR/convert_pssm3.py ${1}.pssm > ${1}.pssm2

       echo "Running jnet"
       $WDIR/jnet_src_v.2.3.1/jnet -H ${1}.hmmat -p ${1}.pssm2 > ${1}.jnet 

    else
       echo "Preparing MSA for hmmer"
       $WDIR/fasta2stockholm.py ${1}.fa ${1}.stockholm
       rm ${1}.hmm
       rm ${1}.prf
       echo "Running hmmer"
       $WDIR/hmmer-2.3.2/src/hmmbuild --fast --gapmax 1.0 --wblosum ${1}.hmm ${1}.stockholm
       $WDIR/hmmer-2.3.2/src/hmmconvert -p ${1}.hmm ${1}.prf
       $WDIR/gcg2hmm3.py ${1}.prf > ${1}.hmmat
       echo "Running jnet"
       $WDIR/jnet_src_v.2.3.1/jnet -H ${1}.hmmat > ${1}.jnet
fi
