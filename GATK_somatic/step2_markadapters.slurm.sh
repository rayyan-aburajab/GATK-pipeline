#!/bin/bash
 
 
#SBATCH --job-name=step2.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step2_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk MarkIlluminaAdapters \
 --I "$DATA_DIR/C083-000002_TumorDNA_fastqtosam.bam" \
 --O "$DATA_DIR/C083-000002_TumorDNA_markilluminaadapters.bam" \
 --M "$DATA_DIR/C083-000002_TumorDNA_markilluminaadapters_metrics.txt"
