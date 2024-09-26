#!/bin/bash
 
 
#SBATCH --job-name=STAR-Fusion.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=96G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=STAR-Fusion_%j.log   # Standard output and error log

FASTQ_DIR="/coh_labs/dits/rayyan/Data/C083-000002/FastqFiles"
OUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/SV_analysis/Star-Fusion"
REF_DIR="/coh_labs/dits/rayyan/References/GRCh38_gencode_v44_CTAT_lib_Oct292023.plug-n-play/ctat_genome_lib_build_dir"
Singularity_STAR="/coh_labs/dits/rayyan/containers/star-fusion.v1.13.0.simg"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec -e "$Singularity_STAR" \
STAR-Fusion \
    --left_fq "$FASTQ_DIR/C083-000002_WF00054603_H036425-01R-01L_TumorRNA_R1_001.fastq.gz" \
    --right_fq "$FASTQ_DIR/C083-000002_WF00054603_H036425-01R-01L_TumorRNA_R2_001.fastq.gz" \
    --genome_lib_dir "$REF_DIR" \
    -O "$OUT_DIR" \
    --FusionInspector validate \
    --examine_coding_effect \
    --denovo_reconstruct