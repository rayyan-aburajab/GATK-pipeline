#!/bin/bash
 
 
#SBATCH --job-name=step3a.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step3a_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
SAMPLE_TYPE="GermlineDNA"
FULL_SAMPLE_NAME="${SAMPLE_NAME}_${SAMPLE_TYPE}"

DATA_DIR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${SAMPLE_TYPE}"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

# Run GATK SamToFastq
singularity exec "$Singularity_GATK" \
gatk SamToFastq \
 --I "$DATA_DIR/${FULL_SAMPLE_NAME}_markilluminaadapters.bam" \
 --FASTQ "$DATA_DIR/${FULL_SAMPLE_NAME}_samtofastq_interleaved.fq" \
 --CLIPPING_ATTRIBUTE XT --CLIPPING_ACTION 2 --INTERLEAVE true --NON_PF true
