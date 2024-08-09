#!/bin/bash
 
 
#SBATCH --job-name=baserecalibration.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=baserecalibration_%j.log   # Standard output and error log

module load singularity

singularity exec -B /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input:/coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input -B /coh_labs/dits/rayyan:/coh_labs/dits/rayyan /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input/gatk.sif \
gatk  BaseRecalibrator \
 --I /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_markedduplicates-addRG.bam \
 --R /coh_labs/dits/rayyan/reference_gatk/Homo_sapiens_assembly38.fasta \
 --known-sites /coh_labs/dits/rayyan/reference_gatk/Homo_sapiens_assembly38.dbsnp138.vcf \
 --known-sites /coh_labs/dits/rayyan/reference_gatk/Homo_sapiens_assembly38.known_indels.vcf.gz \
 --known-sites /coh_labs/dits/rayyan/reference_gatk/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz \
 --O /coh_labs/dits/rayyan/try/recal_data_markdup.table


