#!/bin/bash
 
 
#SBATCH --job-name=step7.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step7_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
SAMPLE_TYPE="GermlineDNA"
FULL_SAMPLE_NAME="${SAMPLE_NAME}_${SAMPLE_TYPE}"

DATA_DIR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${SAMPLE_TYPE}"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
VARIANT_DIR="/coh_labs/dits/rayyan/References/GATK_knownvariants"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

# Run GATK FilterVariantTranches
singularity exec "$Singularity_GATK" \
gatk FilterVariantTranches \
   -V "$DATA_DIR/${FULL_SAMPLE_NAME}_CNNannotated.vcf" \
   --resource "$VARIANT_DIR/hapmap_3.3.hg38.vcf.gz" \
   --resource "$VARIANT_DIR/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz" \
   --info-key CNN_2D \
   --snp-tranche 99.95 \
   --indel-tranche 99.4 \
   --invalidate-previous-filters \
   -O "$DATA_DIR/${FULL_SAMPLE_NAME}_filtervarianttranches.vcf"
