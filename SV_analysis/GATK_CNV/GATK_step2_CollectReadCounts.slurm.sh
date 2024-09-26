#!/bin/bash
 
 
#SBATCH --job-name=GATK_step3.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=GATK_step3_%j.log   # Standard output and error log

GERMLINE_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline"
TUMOR_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
OUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis/GATK_CNV"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
IL_DIR="/coh_labs/dits/rayyan/References/interval_lists"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk CollectReadCounts \
 -I "$GERMLINE_DIR/C083-000002_GermlineDNA_markedduplicates.bam" \
 -L "$IL_DIR/ID2_hg38_tempe_ensembl_v103.targets_preprocessed.interval_list" \
 --interval-merging-rule OVERLAPPING_ONLY \
 -O "$OUT_DIR/C083-000002_GermlineDNA.counts.hdf5"

singularity exec "$Singularity_GATK" \
gatk CollectReadCounts \
 -I "$TUMOR_DIR/C083-000002_TumorDNA_markedduplicates.bam" \
 -L "$IL_DIR/ID2_hg38_tempe_ensembl_v103.targets_preprocessed.interval_list" \
 --interval-merging-rule OVERLAPPING_ONLY \
 -O "$OUT_DIR/C083-000002_TumorDNA.counts.hdf5"