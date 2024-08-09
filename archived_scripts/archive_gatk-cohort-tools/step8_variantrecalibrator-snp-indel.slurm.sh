#!/bin/bash
 
 
#SBATCH --job-name=step8-snp-indel.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step8-snp-indel_%j.log   # Standard output and error log

DATA_DIR="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData2"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
VARIANT_DIR="/coh_labs/dits/rayyan/References/GATK_knownvariants"
Singularity_GATK="/coh_labs/dits/rayyan/containers/gatk_latest.sif"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_GATK" \
gatk VariantRecalibrator \
   -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
   -V "$DATA_DIR/C083-000002_GermlineDNA_genotype.vcf.gz" \
   --resource:hapmap,known=false,training=true,truth=true,prior=15.0 "$VARIANT_DIR/hapmap_3.3.hg38.vcf.gz" \
   --resource:omni,known=false,training=true,truth=false,prior=12.0 "$VARIANT_DIR/1000G_omni2.5.hg38.vcf.gz" \
   --resource:1000G,known=false,training=true,truth=false,prior=10.0 "$VARIANT_DIR/1000G_phase1.snps.high_confidence.hg38.vcf.gz" \
   --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf" \
   -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
   -mode SNP \
   -O "$DATA_DIR/C083-000002_GermlineDNA_VSQR-snp.recal" \
   --tranches-file "$DATA_DIR/C083-000002_GermlineDNA_VSQR-snp.tranches" \
   --rscript-file "$DATA_DIR/C083-000002_GermlineDNA_VSQR-snp.plots.R"

singularity exec "$Singularity_GATK" \
gatk VariantRecalibrator \
   -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
   -V "$DATA_DIR/C083-000002_GermlineDNA_genotype.vcf.gz" \
   --resource:mills,known=false,training=true,truth=true,prior=12.0 "$VARIANT_DIR/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz" \
   --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf" \
   -an QD -an DP -an FS -an SOR -an ReadPosRankSum -an MQRankSum \
   -mode INDEL \
   -O "$DATA_DIR/C083-000002_GermlineDNA_VSQR-indel.recal" \
   --tranches-file "$DATA_DIR/C083-000002_GermlineDNA_VSQR-indel.tranches" \
   --rscript-file "$DATA_DIR/C083-000002_GermlineDNA_VSQR-indel.plots.R"