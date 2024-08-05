# GATK-pipeline

## GATK Best Practices Pipeline Overview

https://gatk.broadinstitute.org/hc/user_images/HWgQodHyIEYYMBG4kxnFyA.jpeg

GATK (4.6.0) singularity container
```
module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

singularity exec "$Singularity_GATK" \
```
## Part I: Sample Pre-Processing

### Step 1: fastq-to-ubam
- Purpose: Generate compatible unmapped bam input for GATK best practices workflow
- Input: Fastq (paired)
- Output: Bam (unmapped)
```
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
Note: the linked guide recommends -M option. This is due to incompatibility between Picard and previous GATK versions. That option is no longer recommended according to more recent documentation.

### Step 3C: mergebamalignment
- Purpose: generates "clean" bam by merging aligned and unmapped bams to retain all meta data
- Input: Bam (unmapped), Bam (mapped), reference
- Output: Bam
```
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
gatk  MarkDuplicatesSpark \
 --I "$DATA_DIR/C083-000002_GermlineDNA_mergebamalignment.bam" \
 --O "$DATA_DIR/C083-000002_GermlineDNA_markedduplicates.bam" \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --M "$DATA_DIR/C083-000002_GermlineDNA_markeddups_metrics.txt
 ```
 Note: may fail due to missing read group information. If so, refer to "optional_addreadgroups" script before marking duplicates.
### Step 5: baserecalibration
[optional - skipping in this workflow]

 ## Part II: Calling GATK Variants

##### Note: the standard best practices workflow is intended for cohorts/multiple samples. Since this analysis involves a single germline sample, some steps differ from the standard protocol. These steps are marked (alt).

### Step 6: haplotypecaller (alt)
- Purpose: identify regions with high variability ("active regions") and align those reads against reference haplotype to assign likely genotypes to each potential variant site
- Input: Bam, reference
- Output: VCF file with raw SNP/indel calls
```
gatk  HaplotypeCaller \
 --I "$DATA_DIR/C083-000002_GermlineDNA_markedduplicates.bam" \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --O "$DATA_DIR/C083-000002_GermlineDNA_haplotypecaller-single.vcf.gz" \
 --bamout "$DATA_DIR/C083-000002_GermlineDNA_haplotypecaller-aligned.bam"
 ```
### Step 7: CNNscorevariants (alt)
- Purpose: uses a pre-trained convolutional neural network (deep learning model) to predict the quality of each variant and annotate accordingly. Here, using 2D model which assesses aligned reads in bam file in addition to reference and variant annotations that are used in 1D model.
- Input: VCF, bam
- Output: VCF file, index file

##### *Issue with GATK docker version 4.6.0.0:* 
*CNNscorevariants stuck on "Loading libgkl_utils.so" step. Same with version 4.5.0.0. Previous discussion forums noted this issue with manual GATK installations that was solved by using docker version (which was 4.2.0.0 at the time). Unclear why my more recent docker containers are not working, but script did eventually work with version 4.2.0.0 (did not try 4.3.0.0 or 4.4.0.0)*
```
gatk CNNScoreVariants \
   -I "$DATA_DIR/C083-000002_GermlineDNA_haplotypecaller-aligned.bam" \
   -V "$DATA_DIR/C083-000002_GermlineDNA_haplotypecaller-single.vcf.gz" \
   -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
   -O "$DATA_DIR/C083-000002_GermlineDNA_CNNannotated.vcf" \
   -tensor-type read_tensor
 ```
### Step 8: filtervarianttranches (alt)
- Purpose: use annotated variant scores (from CNN) and known SNPs/indels (resource input) to filter variants. Here, using default filtering thresholds.
- Input: VCF, known SNP/indel VCFs
- Output: VCF file, index file
```
gatk FilterVariantTranches \
   -V "$DATA_DIR/C083-000002_GermlineDNA_CNNannotated.vcf" \
   --resource "$VARIANT_DIR/hapmap_3.3.hg38.vcf.gz" \
   --resource "$VARIANT_DIR/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz" \
   --info-key CNN_2D \
   --snp-tranche 99.95 \
   --indel-tranche 99.4 \
   --invalidate-previous-filters \
   -O "$DATA_DIR/C083-000002_GermlineDNA_filtervarianttranches.vcf"
 ```
### Step 9: funcotator
- Purpose: annotates variants based on known (gnomAD) datasets.
- Input: VCF
- Output: annotated VCF
```
gatk Funcotator \
     --variant "$DATA_DIR/C083-000002_GermlineDNA_filtervarianttranches.vcf" \
     --reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
     --ref-version hg38 \
     --data-sources-path "$gnomAD_DIR/" \
     --output "$DATA_DIR/C083-000002_GermlineDNA_funcotator.vcf" \
     --output-file-format VCF
 ```
 ### References:
 - Workflow overview: https://gatk.broadinstitute.org/hc/en-us/articles/360035535912-Data-pre-processing-for-variant-discovery
 - Generating ubam from fastq: https://gatk.broadinstitute.org/hc/en-us/articles/4403687183515--How-to-Generate-an-unmapped-BAM-from-FASTQ-or-aligned-BAM
 - Pre-processing guide: https://gatk.broadinstitute.org/hc/en-us/articles/360039568932--How-to-Map-and-clean-up-short-read-sequence-data-efficiently
 - Variant calling guide: https://gatk.broadinstitute.org/hc/en-us/articles/360035535932-Germline-short-variant-discovery-SNPs-Indels