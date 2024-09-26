#!/bin/bash
 
 
#SBATCH --job-name=GATK_step4b.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=GATK_step4b_%j.log   # Standard output and error log

OUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis/GATK_CNV"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk PlotDenoisedCopyRatios \
 --standardized-copy-ratios "$OUT_DIR/C083-000002_TumorDNA_standardizedCR.tsv" \
 --denoised-copy-ratios "$OUT_DIR/C083-000002_TumorDNA_denoisedCR.tsv" \
 --sequence-dictionary "$REF_DIR/Homo_sapiens_assembly38.dict" \
 --minimum-contig-length 46709983 \
 --output "$OUT_DIR/plots" \
 --output-prefix C083-000002_TumorDNA