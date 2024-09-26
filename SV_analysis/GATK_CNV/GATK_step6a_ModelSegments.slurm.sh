#!/bin/bash
 
 
#SBATCH --job-name=GATK_step6a.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=96G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=GATK_step6a_%j.log   # Standard output and error log


OUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis/GATK_CNV"
IL_DIR="/coh_labs/dits/rayyan/References/interval_lists"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk --java-options "-Xmx80g" ModelSegments \
 --denoised-copy-ratios "$OUT_DIR/C083-000002_TumorDNA_denoisedCR.tsv" \
 --allelic-counts "$OUT_DIR/C083-000002_TumorDNA.allelicCounts.tsv" \
 --normal-allelic-counts "$OUT_DIR/C083-000002_GermlineDNA.allelicCounts.tsv" \
 --output "$OUT_DIR/modelsegments" \
 --output-prefix C083-000002_TumorDNA