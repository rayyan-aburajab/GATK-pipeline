#!/bin/bash
 
 
#SBATCH --job-name=step3b.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step3b_%j.log   # Standard output and error log

module load BWA/0.7.17-GCCcore-5.4.0 

bwa mem -p /coh_labs/dits/rayyan/reference_gatk/Homo_sapiens_assembly38.fasta \
/coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_samtofastq_interleaved.fq > /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_bwamem.sam
