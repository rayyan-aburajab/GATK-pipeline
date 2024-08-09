#!/bin/bash
 
 
#SBATCH --job-name=align3-mergebam_redo.sh    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=raburajab@coh.org     # Where to send mail
#SBATCH -n 8                          # Number of cores
#SBATCH -N 1-1                        # Min - Max Nodes
#SBATCH --mem=32G                      # Amount of memory in GB
#SBATCH --time=24:00:00               # Time limit hrs:min:sec
#SBATCH --output=align3-mergebam_redo%j.log   # Standard output and error log

module load singularity

singularity exec -B /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input:/coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input -B /coh_labs/dits/rayyan:/coh_labs/dits/rayyan /coh_labs/dits/ngs_tools/ORIEN_ADMIXTURE/input/gatk.sif \
gatk  MergeBamAlignment \
 --R /coh_labs/dits/rayyan/reference_gatk/Homo_sapiens_assembly38.fasta \
 --ALIGNED_BAM /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_bwamem.sam \
 --UNMAPPED_BAM /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_markilluminaadapters.bam \
 --OUTPUT /coh_labs/dits/rayyan/try/C083-000002_GermlineDNA_mergebamalignment.bam \
 --CREATE_INDEX true \
 --CLIP_ADAPTERS false --CLIP_OVERLAPPING_READS true \
 --INCLUDE_SECONDARY_ALIGNMENTS true --MAX_INSERTIONS_OR_DELETIONS -1 \
 --PRIMARY_ALIGNMENT_STRATEGY MostDistant --ATTRIBUTES_TO_RETAIN XS
