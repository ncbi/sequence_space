# sequence_space
Code and data from "Many dissimilar protein domains switch between alpha-helix and beta-sheet folds"

JPred_predictions contains code used to make fold-switch predictions.  Dependencies:

hmmer-2.3.2: http://hmmer.org/download.html  
mview-1.67: https://sourceforge.net/projects/bio-mview/files/bio-mview/mview-1.67/  
blast 2.2.26: https://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/   
jnet_src_v.2.3.1: https://www.compbio.dundee.ac.uk/jpred/about.shtml  
python3: https://www.python.org/downloads/  

python3 libraries required to run code:  
matplotlib  
pandas 
numpy  
biopython  
networkx  
scikit-learn 

Typical install time: 30 minutes-1 hour.

Note that PSI-BLAST was run on sequences with the following command:  
psiblast -db database -num_iterations 3 -num_alignments 10000 -num_threads 16 -query ID/ID.fasta -out ID/ID.bla7 -evalue 0.05 -outfmt "7 qaccver saccver pident length mismatch gapopen qstart qend sstart send evalue bitscore qseq sseq staxid sscinames" -out_ascii_pssm ID/ID.pssm  

databases were either uniref90: https://ftp.uniprot.org/pub/databases/uniprot/previous_releases/release-2020_06/uniref/
or jpred: https://www.compbio.dundee.ac.uk/jpred/about_RETR_JNetv231_details.shtml

Structure of data to be analyzed: DataDirectory/UniprotID/UniprotID.fa  
Each sequence from Uniprot has its own folder, named by Uniprot ID.  Within that folder, its sequence is saved in fasta (.fa) format, with named by  
Uniprot ID

Pipeline with all code was tested on Linux RHEL/CentOS6
collate_preds_final.py was also tested on macOS Catalina 10.15.7
