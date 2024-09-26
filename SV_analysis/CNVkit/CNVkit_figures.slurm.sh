#!/bin/bash
 
 
#SBATCH --job-name=CNVkit.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=figs_CNVkit_%j.log   # Standard output and error log

OUTPUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis"
Singularity_CNVkit="/coh_labs/dits/rayyan/containers/cnvkit_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
# singularity exec "$Singularity_CNVkit" \
# cnvkit.py scatter "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.cnr" -s "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.cns" \
#     -o "$OUTPUT_DIR/C083-000002_TumorDNA_scatter.pdf"

# singularity exec "$Singularity_CNVkit" \
# cnvkit.py diagram -t -s "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.cns" \
#     -o "$OUTPUT_DIR/C083-000002_TumorDNA_diagram.pdf"

# singularity exec "$Singularity_CNVkit" \
# cnvkit.py heatmap "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.cns" \
#     -o "$OUTPUT_DIR/C083-000002_TumorDNA_heatmap.pdf"

singularity exec "$Singularity_CNVkit" \
cnvkit.py genemetrics "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.cnr" \
    -o "$OUTPUT_DIR/C083-000002_TumorDNA_genemetrics.txt"