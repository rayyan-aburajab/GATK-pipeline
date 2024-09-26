#!/bin/bash
 
 
#SBATCH --job-name=step5a.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=64G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step5a_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
NORMAL_TYPE="GermlineDNA"
TUMOR_TYPE="TumorDNA"
FULL_SAMPLE_NAME_NORMAL="${SAMPLE_NAME}_${NORMAL_TYPE}"
FULL_SAMPLE_NAME_TUMOR="${SAMPLE_NAME}_${TUMOR_TYPE}"

DATA_DIR_NORMAL="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${NORMAL_TYPE}"
DATA_DIR_TUMOR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${TUMOR_TYPE}"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_strelka="/coh_labs/dits/rayyan/containers/strelka2-manta_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

singularity exec "$Singularity_strelka" \
configureStrelkaSomaticWorkflow.py \
 --normalBam "$DATA_DIR_NORMAL/${FULL_SAMPLE_NAME_NORMAL}_markedduplicates.bam" \
 --tumorBam "$DATA_DIR_TUMOR/${FULL_SAMPLE_NAME_TUMOR}_markedduplicates.bam" \
 --referenceFasta "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --runDir "$DATA_DIR_TUMOR"