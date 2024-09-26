#!/bin/bash
 
 
#SBATCH --job-name=GATK_step5.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=GATK_step5_%j.log   # Standard output and error log

GERMLINE_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline"
TUMOR_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
OUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis/GATK_CNV"
IL_DIR="/coh_labs/dits/rayyan/References/interval_lists"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk CollectAllelicCounts \
 -I "$GERMLINE_DIR/C083-000002_GermlineDNA_markedduplicates.bam" \
 -L "$IL_DIR/ID2_hg38_tempe_ensembl_v103.targets_preprocessed.interval_list" \
 -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 -O "$OUT_DIR/C083-000002_GermlineDNA.allelicCounts.tsv"
 
singularity exec "$Singularity_GATK" \
gatk CollectAllelicCounts \
 -I "$TUMOR_DIR/C083-000002_TumorDNA_markedduplicates.bam" \
 -L "$IL_DIR/ID2_hg38_tempe_ensembl_v103.targets_preprocessed.interval_list" \
 -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 -O "$OUT_DIR/C083-000002_TumorDNA.allelicCounts.tsv"