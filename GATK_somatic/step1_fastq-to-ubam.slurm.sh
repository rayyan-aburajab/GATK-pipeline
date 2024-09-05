#!/bin/bash
 
 
#SBATCH --job-name=step1.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step1_%j.log   # Standard output and error log

FASTQ_DIR="/coh_labs/dits/rayyan/Data/C083-000002/FastqFiles"
OUTPUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk FastqToSam \
 --FASTQ "$FASTQ_DIR/C083-000002_WF00054603_H036425-02D-01L_TumorDNA_R1_001.fastq.gz" \
 --FASTQ2 "$FASTQ_DIR/C083-000002_WF00054603_H036425-02D-01L_TumorDNA_R2_001.fastq.gz" \
 --OUTPUT "$OUTPUT_DIR/C083-000002_TumorDNA_fastqtosam.bam" \
 --SAMPLE_NAME C083-000002_TumorDNA
