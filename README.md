# GATK-pipeline

## GATK Best Practices Pipeline Overview

https://gatk.broadinstitute.org/hc/theming_assets/01HZPKW2HXTR2JFMVD55S4VNTY

GATK (4.6.0) singularity container
```
module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"
```
## Sample Pre-Processing

### Step 1: fastq-to-ubam
- Purpose: Generate compatible unmapped bam input for GATK best practices workflow
- Input: Fastq (paired)
- Output: Bam (unmapped)
```
singularity exec "$Singularity_GATK" \
gatk FastqToSam \
 --FASTQ "$FASTQ_DIR/C083-000002_WF00054603_h034885-01D-01L_GermlineDNA_R1_001.fastq.gz" \
 --FASTQ2 "$FASTQ_DIR/C083-000002_WF00054603_h034885-01D-01L_GermlineDNA_R2_001.fastq.gz" \
 --OUTPUT "$OUTPUT_DIR/C083-000002_GermlineDNA_fastqtosam.bam" \
 --SAMPLE_NAME C083-000002_GermlineDNA
 ```
### Step 2: markadapters
- Purpose: Mark adapter sequences within reads, which arise through concatenation of adapters or readthrough of short reads
- Input: Bam (unmapped)
- Output: Bam (unmapped), metrics file
```
singularity exec "$Singularity_GATK" \
gatk MarkIlluminaAdapters \
 --I "$DATA_DIR/C083-000002_GermlineDNA_fastqtosam.bam" \
 --O "$DATA_DIR/C083-000002_GermlineDNA_markilluminaadapters.bam" \
 --M "$DATA_DIR/C083-000002_GermlineDNA_markilluminaadapters_metrics.txt"
 ```
### Step 3A: ubam-to-fastq
- Purpose: Generates a fastq file (R1+2 combined) with adapter sequences removed
- Input: Bam (unmapped)
- Output: Fastq (interleaved)
```
singularity exec "$Singularity_GATK" \
gatk  SamToFastq \
 --I "$DATA_DIR/C083-000002_GermlineDNA_markilluminaadapters.bam" \
 --FASTQ "$DATA_DIR/C083-000002_GermlineDNA_samtofastq_interleaved.fq" \
 --CLIPPING_ATTRIBUTE XT --CLIPPING_ACTION 2 --INTERLEAVE true --NON_PF true
 ```
### Step 3B: bwamem-alignment
- Purpose: Aligns sample to reference genome
- Input: Fastq (interleaved), reference
- Output: Bam (mapped)
```
bwa mem -p "$REF_DIR"/Homo_sapiens_assembly38.fasta \
"$DATA_DIR/C083-000002_GermlineDNA_samtofastq_interleaved.fq" > "$DATA_DIR/C083-000002_GermlineDNA_bwamem.sam"
```
### Step 3C: mergebamalignment
- Purpose: generates "clean" bam by merging aligned and unmapped bams to retain all meta data
- Input: Bam (unmapped), Bam (mapped), reference
- Output: Bam
```
singularity exec "$Singularity_GATK" \
gatk  MergeBamAlignment \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --ALIGNED_BAM "$DATA_DIR/C083-000002_GermlineDNA_bwamem.sam" \
 --UNMAPPED_BAM "$DATA_DIR/C083-000002_GermlineDNA_markilluminaadapters.bam" \
 --OUTPUT "$DATA_DIR/C083-000002_GermlineDNA_mergebamalignment.bam" \
 --CREATE_INDEX true --ADD_MATE_CIGAR true \
 --CLIP_ADAPTERS false --CLIP_OVERLAPPING_READS true \
 --INCLUDE_SECONDARY_ALIGNMENTS true --MAX_INSERTIONS_OR_DELETIONS -1 \
 --PRIMARY_ALIGNMENT_STRATEGY MostDistant --ATTRIBUTES_TO_RETAIN XS
 ```
### Step 4: markduplicates
- Purpose: identify and label read duplicates that are non-independent measurements (e.g. PCR) and choose one representative read to be used for subsequence analyses
- Input: Bam, reference
- Output: Bam, metrics file
```
singularity exec "$Singularity_GATK" \
gatk  MarkDuplicatesSpark \
 --I "$DATA_DIR/C083-000002_GermlineDNA_mergebamalignment.bam" \
 --O "$DATA_DIR/C083-000002_GermlineDNA_markedduplicates.bam" \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --M "$DATA_DIR/C083-000002_GermlineDNA_markeddups_metrics.txt
 ```
### Step 5: baserecalibration
[skipping in this workflow]

 ## Calling GATK Variants

### Step 6:
(to be continued)


 ### References:
 - Workflow overview: https://gatk.broadinstitute.org/hc/en-us/articles/360035535912-Data-pre-processing-for-variant-discovery
 - Generating ubam from fastq: https://gatk.broadinstitute.org/hc/en-us/articles/4403687183515--How-to-Generate-an-unmapped-BAM-from-FASTQ-or-aligned-BAM
 - Pre-processing guide: https://gatk.broadinstitute.org/hc/en-us/articles/360039568932--How-to-Map-and-clean-up-short-read-sequence-data-efficiently
 - 