#!/bin/bash
 
 
#SBATCH --job-name=step5a.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=64G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=step5a_%j.log   # Standard output and error log

DATA_DIR_normal="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline"
DATA_DIR_tumor="/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_TumorDNA"
REF_DIR="/coh_labs/dits/rayyan/References/GATK_assembly38"
Singularity_strelka="/coh_labs/dits/rayyan/containers/strelka2-manta_latest.sif"
#RUN_DIR="/coh_labs/dits/rayyan/Projects/GATK-pipeline/GATK_somatic"

module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
 
singularity exec "$Singularity_strelka" \
configureStrelkaSomaticWorkflow.py \
 --normalBam "$DATA_DIR_normal/C083-000002_GermlineDNA_markedduplicates.bam" \
 --tumorBam "$DATA_DIR_tumor/C083-000002_TumorDNA_markedduplicates.bam" \
 --referenceFasta "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --runDir "$DATA_DIR_tumor"