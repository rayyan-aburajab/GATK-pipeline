#!/bin/bash
 
 
#SBATCH --job-name=optional_addreadgroup.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=optional_addreadgroup_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData2"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs:/coh_labs"
 
singularity exec "$Singularity_GATK" \
gatk  AddOrReplaceReadGroups \
 --I "$DATA_DIR/C083-000002_GermlineDNA_mergebamalignment.bam" \
 --O "$DATA_DIR/C083-000002_GermlineDNA_mergebamalignment_addRG.bam" \
 --RGLB lib1 \
 --RGPL ILLUMINA \
 --RGPU unit1 \
 --RGSM sample \
 --CREATE_INDEX true
