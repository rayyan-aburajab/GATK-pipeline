#!/bin/bash
 
 
#SBATCH --job-name=step9a.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step9a_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData2"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
VARIANT_DIR="/coh_labs/dits/rayyan/References/GATK_knownvariants"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk CalculateGenotypePosteriors \
   -V "$DATA_DIR/C083-000002_GermlineDNA_filteredvariants.vcf" \
   -O "$DATA_DIR/C083-000002_GermlineDNA_refine-posteriors.vcf.gz" \
   -supporting "$VARIANT_DIR/1000G_phase3_v4_20130502.sites.hg38.vcf"