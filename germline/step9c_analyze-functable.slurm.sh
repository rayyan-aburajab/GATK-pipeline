#!/bin/bash
 
 
#SBATCH --job-name=step9c.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step9c_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData2"

cat "$DATA_DIR/C083-000002_GermlineDNA_funcotator.vcf" | grep " Funcotation fields are: " | sed 's/|/\t/g' > "$DATA_DIR/C083-000002_GermlineDNA_func-variants.txt"

cat "$DATA_DIR/C083-000002_GermlineDNA_funcotator_output.table" | cut -f 16 | sed 's/|/\t/g' >> "$DATA_DIR/C083-000002_GermlineDNA_func-variants.txt"
