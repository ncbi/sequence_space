#! /bin/bash

cat ${1}.fa > ${1}.bla7.f

F=${1}.pssm
if test -f "$F"
    then
       cp ${1}.fa ${1}.bla7.fa
       /home/porterll/programs/mview -out fasta ${1}.bla7 >> ${1}.bla7.fa
       /data/porterll/sequence_space/fix_MSA.py ${1}.bla7.fa > ${1}.forhmmer
       /data/porterll/sequence_space/fasta2stockholm.py ${1}.forhmmer ${1}.stockholm
       rm ${1}.hmm
       rm ${1}.prf
       /home/porterll/hmmer-2.3.2/src/hmmbuild --fast --gapmax 1.0 --wblosum ${1}.hmm ${1}.stockholm
       /home/porterll/hmmer-2.3.2/src/hmmconvert -p ${1}.hmm ${1}.prf
       /data/porterll/sequence_space/gcg2hmm.py ${1}.prf > ${1}.hmmat

       /data/porterll/sequence_space/convert_pssm.py ${1}.pssm > ${1}.pssm2

       /home/porterll/programs/jnet_src_v.2.3.1/jnet -H ${1}.hmmat -p ${1}.pssm2 > ${1}.jnet 

    else
       /data/porterll/sequence_space/fasta2stockholm.py ${1}.fa ${1}.stockholm
       rm ${1}.hmm
       rm ${1}.prf
       /home/porterll/hmmer-2.3.2/src/hmmbuild --fast --gapmax 1.0 --wblosum ${1}.hmm ${1}.stockholm
       /home/porterll/hmmer-2.3.2/src/hmmconvert -p ${1}.hmm ${1}.prf
       /data/porterll/sequence_space/gcg2hmm.py ${1}.prf > ${1}.hmmat
       /home/porterll/programs/jnet_src_v.2.3.1/jnet -H ${1}.hmmat > ${1}.jnet
fi
