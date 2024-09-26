#!/bin/bash
 
 
#SBATCH --job-name=step3b.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step3b_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
SAMPLE_TYPE="TumorDNA"
FULL_SAMPLE_NAME="${SAMPLE_NAME}_${SAMPLE_TYPE}"

DATA_DIR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${SAMPLE_TYPE}"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"

module load BWA/0.7.17-GCCcore-5.4.0

bwa mem -p "$REF_DIR/Homo_sapiens_assembly38.fasta" \
"$DATA_DIR/${FULL_SAMPLE_NAME}_samtofastq_interleaved.fq" > "$DATA_DIR/${FULL_SAMPLE_NAME}_bwamem.sam"
