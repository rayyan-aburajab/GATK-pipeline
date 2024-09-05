#!/bin/bash
 
 
#SBATCH --job-name=step8.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=16G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step8_%j.log   # Standard output and error log

#DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA"

Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"
VARIANT_DIR="/coh_labs/dits/rayyan/References/GATK_knownvariants"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk VariantAnnotator \
    -V "$DATA_DIR/somatic.snvs.filtered.funcotator.vcf" \
    -reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
    -O "$DATA_DIR/somatic.snvs.filtered.funcotator-dbsnp.vcf" \
    -dbsnp "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"

singularity exec "$Singularity_GATK" \
gatk VariantAnnotator \
    -V "$DATA_DIR/somatic.indels.filtered.funcotator.vcf" \
    -reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
    -O "$DATA_DIR/somatic.indels.filtered.funcotator-dbsnp.vcf" \
    -dbsnp "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"