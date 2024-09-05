#!/bin/bash
 
 
#SBATCH --job-name=step7b.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step7b_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA/results/variants"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
gnomAD_DIR="/coh_labs/dits/rayyan/References/GATK_gnomAD/funcotator_dataSources.v1.8.hg38.20230908s"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk Funcotator \
     --variant "$DATA_DIR/somatic.snvs.filtered.vcf" \
     --reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
     --ref-version hg38 \
     --data-sources-path "$gnomAD_DIR/" \
     --output "$DATA_DIR/somatic.snvs.filtered.funcotator.vcf" \
     --output-file-format VCF

singularity exec "$Singularity_GATK" \
gatk Funcotator \
     --variant "$DATA_DIR/somatic.indels.filtered.vcf" \
     --reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
     --ref-version hg38 \
     --data-sources-path "$gnomAD_DIR/" \
     --output "$DATA_DIR/somatic.indels.filtered.funcotator.vcf" \
     --output-file-format VCF