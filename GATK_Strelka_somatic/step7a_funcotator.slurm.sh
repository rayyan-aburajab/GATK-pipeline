#!/bin/bash
 
 
#SBATCH --job-name=step7a.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step7a-download_%j.log   # Standard output and error log

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"
 
singularity exec "$Singularity_GATK" \
gatk FuncotatorDataSourceDownloader --somatic --hg38 --validate-integrity --extract-after-download