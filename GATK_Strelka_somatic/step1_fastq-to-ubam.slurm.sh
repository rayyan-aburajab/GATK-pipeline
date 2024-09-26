#!/bin/bash
 
 
#SBATCH --job-name=step1.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step1_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
SAMPLE_TYPE="TumorDNA"
FULL_SAMPLE_NAME="${SAMPLE_NAME}_${SAMPLE_TYPE}"

FASTQ_DIR="/coh_labs/dits/rayyan/Data/FastqFiles"
OUTPUT_DIR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${SAMPLE_TYPE}"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

FASTQ_R1=""
FASTQ_R2=""

for gz in "$FASTQ_DIR"/*.fastq.gz; do
  if [[ "$gz" == *"${SAMPLE_NAME}"* && "$gz" == *"${SAMPLE_TYPE}"* ]]; then
    if [[ "$gz" == *R1* ]]; then
      FASTQ_R1="$gz"
    elif [[ "$gz" == *R2* ]]; then
      FASTQ_R2="$gz"
    fi
  fi
done

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

singularity exec "$Singularity_GATK" \
gatk FastqToSam \
 --FASTQ "$FASTQ_R1" \
 --FASTQ2 "$FASTQ_R2" \
 --OUTPUT "$OUTPUT_DIR/${FULL_SAMPLE_NAME}_fastqtosam.bam" \
 --SAMPLE_NAME "$FULL_SAMPLE_NAME"
