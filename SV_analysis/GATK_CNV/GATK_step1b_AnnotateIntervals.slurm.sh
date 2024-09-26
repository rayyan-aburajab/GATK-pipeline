#!/bin/bash
 
 
#SBATCH --job-name=GATK_step2.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=GATK_step2_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis/GATK_CNV"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
IL_DIR="/coh_labs/dits/rayyan/References/interval_lists"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk AnnotateIntervals \
 -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 -L "$IL_DIR/ID2_hg38_tempe_ensembl_v103.targets_preprocessed.interval_list" \
 --interval-merging-rule OVERLAPPING_ONLY \
 -O "$IL_DIR/ID2_hg38_tempe_ensembl_v103.targets_annotated.intervals.tsv"