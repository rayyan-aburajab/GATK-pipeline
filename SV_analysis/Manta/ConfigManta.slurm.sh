#!/bin/bash
 
 
#SBATCH --job-name=ConfigManta.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=ConfigManta_%j.log   # Standard output and error log

NORMAL_BAM="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_markedduplicates.bam"
TUMOR_BAM="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA/C083-000002_TumorDNA_markedduplicates.bam"
OUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/SV_analysis/Manta_exome"
REF="/coh_labs/dits/rayyan/References/GATK_assembly38/Homo_sapiens_assembly38.fasta"
Singularity_Manta="/coh_labs/dits/rayyan/containers/strelka2-manta_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_Manta" \
configManta.py \
  --normalBam $NORMAL_BAM \
  --tumorBam $TUMOR_BAM \
  --referenceFasta $REF \
  --runDir $OUT_DIR \
  --exome