#!/bin/bash
 
 
#SBATCH --job-name=step6.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step6_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
SAMPLE_TYPE="GermlineDNA"
FULL_SAMPLE_NAME="${SAMPLE_NAME}_${SAMPLE_TYPE}"

DATA_DIR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${SAMPLE_TYPE}"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_4.2.0.0.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

# Run GATK CNNScoreVariants
singularity exec "$Singularity_GATK" \
gatk CNNScoreVariants \
   -I "$DATA_DIR/${FULL_SAMPLE_NAME}_haplotypecaller.bam" \
   -V "$DATA_DIR/${FULL_SAMPLE_NAME}_haplotypecaller.vcf.gz" \
   -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
   -O "$DATA_DIR/${FULL_SAMPLE_NAME}_CNNannotated.vcf" \
   -tensor-type read_tensor