#!/bin/bash
 
 
#SBATCH --job-name=addreadgroup.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=addreadgroup%j.log   # Standard output and error log

module load singularity

singularity exec -B /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input:/coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input -B /coh_labs/dits/rayyan:/coh_labs/dits/rayyan /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input/gatk.sif \
gatk  AddOrReplaceReadGroups \
 --I C083-000002_GermlineDNA_markedduplicates.bam \
 --O C083-000002_GermlineDNA_markedduplicates-addRG.bam \
 --RGLB lib1 \
 --RGPL ILLUMINA \
 --RGPU unit1 \
 --RGSM sample \
 --CREATE_INDEX true
