#!/bin/bash
 
 
#SBATCH --job-name=step7.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step7_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData2"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk GenotypeGVCFs \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --V "$DATA_DIR/C083-000002_GermlineDNA_haplotypecaller.g.vcf.gz" \
 --O "$DATA_DIR/C083-000002_GermlineDNA_genotype.vcf.gz"