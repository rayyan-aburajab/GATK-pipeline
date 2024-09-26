#!/bin/bash
 
 
#SBATCH --job-name=CNVkit.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=CNVkit_export_%j.log   # Standard output and error log

OUTPUT_DIR="/coh_labs/dits/rayyan/Data/C083-000002/CNV_analysis"
Singularity_CNVkit="/coh_labs/dits/rayyan/containers/cnvkit_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_CNVkit" \
cnvkit.py export bed "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.cns"  \
    --show all -o "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.bed"

singularity exec "$Singularity_CNVkit" \
cnvkit.py export vcf "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.cns" \
    -x male -i "C083-000002_TumorDNA" -o "$OUTPUT_DIR/C083-000002_TumorDNA_markedduplicates.call.vcf"
