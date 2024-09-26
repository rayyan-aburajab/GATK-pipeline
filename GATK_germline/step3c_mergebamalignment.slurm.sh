#!/bin/bash
 
 
#SBATCH --job-name=step3c.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step3c_%j.log   # Standard output and error log

SAMPLE_NAME="C083-000120"
SAMPLE_TYPE="GermlineDNA"
FULL_SAMPLE_NAME="${SAMPLE_NAME}_${SAMPLE_TYPE}"

DATA_DIR="/coh_labs/dits/rayyan/Data/${SAMPLE_NAME}/AnalysisData_${SAMPLE_TYPE}"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

# Run GATK MergeBamAlignment
singularity exec "$Singularity_GATK" \
gatk MergeBamAlignment \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --ALIGNED_BAM "$DATA_DIR/${FULL_SAMPLE_NAME}_bwamem.sam" \
 --UNMAPPED_BAM "$DATA_DIR/${FULL_SAMPLE_NAME}_markilluminaadapters.bam" \
 --OUTPUT "$DATA_DIR/${FULL_SAMPLE_NAME}_mergebamalignment.bam" \
 --CREATE_INDEX true --ADD_MATE_CIGAR true \
 --CLIP_ADAPTERS false --CLIP_OVERLAPPING_READS true \
 --INCLUDE_SECONDARY_ALIGNMENTS true --MAX_INSERTIONS_OR_DELETIONS -1 \
 --PRIMARY_ALIGNMENT_STRATEGY MostDistant --ATTRIBUTES_TO_RETAIN XS
