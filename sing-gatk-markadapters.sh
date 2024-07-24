#!/bin/bash
 
 
#SBATCH --job-name=markadapters.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=markadapters_%j.log   # Standard output and error log

module load singularity

singularity exec -B /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input:/coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input -B /coh_labs/dits/rayyan/try:/coh_labs/dits/rayyan/try /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input/gatk.sif \
gatk MarkIlluminaAdapters \
 --I /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_fastqtosam.bam \
 --O /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_markilluminaadapters.bam \
 --M /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_markilluminaadapters_metrics.txt
