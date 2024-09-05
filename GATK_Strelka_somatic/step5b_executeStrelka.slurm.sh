#!/bin/bash
 
 
#SBATCH --job-name=step5b.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=64G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step5b_%j.log   # Standard output and error log

DATA_DIR_tumor="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
Singularity_strelka="/coh_labs/dits/rayyan/containers/strelka2-manta_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_strelka" \
"$DATA_DIR_tumor/runWorkflow.py" \
 --mode local \
 --jobs 8