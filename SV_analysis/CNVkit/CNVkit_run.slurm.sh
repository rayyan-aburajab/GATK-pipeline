#!/bin/bash
 
 
#SBATCH --job-name=CNVkit.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=CNVkit_%j.log   # Standard output and error log

REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
OUTPUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis"
Singularity_CNVkit="/coh_labs/dits/rayyan/containers/cnvkit_latest.sif"

NORMAL_BAM="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_markedduplicates.bam"
TUMOR_BAM="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA/C083-000002_TumorDNA_markedduplicates.bam"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_CNVkit" \
cnvkit.py batch "$TUMOR_BAM" --normal "$NORMAL_BAM" \
    --method wgs --output-dir "$OUTPUT_DIR" \
    --fasta "$REF_DIR/Homo_sapiens_assembly38.fasta" --annotate "$REF_DIR/refFlat.txt"