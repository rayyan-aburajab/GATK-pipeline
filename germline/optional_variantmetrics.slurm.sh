#!/bin/bash
 
 
#SBATCH --job-name=step11c.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step11c_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"
VARIANT_DIR="/coh_labs/dits/rayyan/References/GATK_knownvariants"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk CollectVariantCallingMetrics \
 -I "$DATA_DIR/C083-000002_GermlineDNA_func_splitSNP_dbsnp.vcf" \
 -O "$DATA_DIR/C083-000002_GermlineDNA_func_splitSNP_dbsnp" \
 -DBSNP "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"

singularity exec "$Singularity_GATK" \
gatk CollectVariantCallingMetrics \
 -I "$DATA_DIR/C083-000002_GermlineDNA_func_splitINDEL_dbsnp.vcf" \
 -O "$DATA_DIR/C083-000002_GermlineDNA_func_splitINDEL_dbsnp" \
 -DBSNP "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"