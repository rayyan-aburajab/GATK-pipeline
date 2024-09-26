# GATK-pipeline

## GATK Best Practices Pipeline Overview

https://gatk.broadinstitute.org/hc/user_images/HWgQodHyIEYYMBG4kxnFyA.jpeg

How to call GATK (4.6.0) singularity container:
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
 --FASTQ "$FASTQ_R1" \
 --FASTQ2 "$FASTQ_R2" \
 --OUTPUT "$OUTPUT_DIR/${FULL_SAMPLE_NAME}_fastqtosam.bam" \
 --SAMPLE_NAME "$FULL_SAMPLE_NAME"
 ```
### Step 2: markadapters
- Purpose: Mark adapter sequences within reads, which arise through concatenation of adapters or readthrough of short reads
- Input: Bam (unmapped)
- Output: Bam (unmapped), metrics file
```
gatk MarkIlluminaAdapters \
 --I "$DATA_DIR/${FULL_SAMPLE_NAME}_fastqtosam.bam" \
 --O "$DATA_DIR/${FULL_SAMPLE_NAME}_markilluminaadapters.bam" \
 --M "$DATA_DIR/${FULL_SAMPLE_NAME}_markilluminaadapters_metrics.txt"
 ```
### Step 3A: ubam-to-fastq
- Purpose: Generates a fastq file (R1+2 combined) with adapter sequences removed
- Input: Bam (unmapped)
- Output: Fastq (interleaved)
```
gatk SamToFastq \
 --I "$DATA_DIR/${FULL_SAMPLE_NAME}_markilluminaadapters.bam" \
 --FASTQ "$DATA_DIR/${FULL_SAMPLE_NAME}_samtofastq_interleaved.fq" \
 --CLIPPING_ATTRIBUTE XT --CLIPPING_ACTION 2 --INTERLEAVE true --NON_PF true
 ```
### Step 3B: bwamem-alignment
- Purpose: Aligns sample to reference genome
- Input: Fastq (interleaved), reference
- Output: Bam (mapped)
```
bwa mem -p "$REF_DIR/Homo_sapiens_assembly38.fasta" \
"$DATA_DIR/${FULL_SAMPLE_NAME}_samtofastq_interleaved.fq" > "$DATA_DIR/${FULL_SAMPLE_NAME}_bwamem.sam"
```
Note: the linked guide recommends -M option. This is due to incompatibility between Picard and previous GATK versions. That option is no longer recommended according to more recent documentation.

### Step 3C: mergebamalignment
- Purpose: generates "clean" bam by merging aligned and unmapped bams to retain all meta data
- Input: Bam (unmapped), Bam (mapped), reference
- Output: Bam
```
gatk MergeBamAlignment \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --ALIGNED_BAM "$DATA_DIR/${FULL_SAMPLE_NAME}_bwamem.sam" \
 --UNMAPPED_BAM "$DATA_DIR/${FULL_SAMPLE_NAME}_markilluminaadapters.bam" \
 --OUTPUT "$DATA_DIR/${FULL_SAMPLE_NAME}_mergebamalignment.bam" \
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
gatk MarkDuplicatesSpark \
 --I "$DATA_DIR/${FULL_SAMPLE_NAME}_mergebamalignment.bam" \
 --O "$DATA_DIR/${FULL_SAMPLE_NAME}_markedduplicates.bam" \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --M "$DATA_DIR/${FULL_SAMPLE_NAME}_markeddups_metrics.txt"
 ```

 ## Part II: Calling GATK Variants

##### Note: the standard best practices workflow is intended for cohorts/multiple samples. Since this analysis involves a single germline sample, some steps differ from the standard protocol. These steps are marked (alt).

### Step 5: haplotypecaller (alt)
- Purpose: identify regions with high variability ("active regions") and align those reads against reference haplotype to assign likely genotypes to each potential variant site
- Input: Bam, reference
- Output: VCF file with raw SNP/indel calls
```
gatk HaplotypeCaller \
 --I "$DATA_DIR/${FULL_SAMPLE_NAME}_markedduplicates.bam" \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --O "$DATA_DIR/${FULL_SAMPLE_NAME}_haplotypecaller.vcf.gz" \
 --bamout "$DATA_DIR/${FULL_SAMPLE_NAME}_haplotypecaller.bam"
 ```
### Step 6: CNNscorevariants (alt)
- Purpose: uses a pre-trained convolutional neural network (deep learning model) to predict the quality of each variant and annotate accordingly. Here, using 2D model which assesses aligned reads in bam file in addition to reference and variant annotations that are used in 1D model.
- Input: VCF, bam
- Output: VCF file, index file

##### *Issue with GATK docker version 4.6.0.0:* 
*CNNscorevariants stuck on "Loading libgkl_utils.so" step. Same with version 4.5.0.0. Previous discussion forums noted this issue with manual GATK installations that was solved by using docker version (which was 4.2.0.0 at the time). Unclear why my more recent docker containers are not working, but script did eventually work with version 4.2.0.0 (did not try 4.3.0.0 or 4.4.0.0)*
```
gatk CNNScoreVariants \
   -I "$DATA_DIR/${FULL_SAMPLE_NAME}_haplotypecaller.bam" \
   -V "$DATA_DIR/${FULL_SAMPLE_NAME}_haplotypecaller.vcf.gz" \
   -R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
   -O "$DATA_DIR/${FULL_SAMPLE_NAME}_CNNannotated.vcf" \
   -tensor-type read_tensor
 ```
### Step 7: filtervarianttranches (alt)
- Purpose: use annotated variant scores (from CNN) and known SNPs/indels (resource input) to filter variants. Here, using default filtering thresholds.
- Input: VCF, known SNP/indel VCFs
- Output: VCF file, index file
```
gatk FilterVariantTranches \
   -V "$DATA_DIR/${FULL_SAMPLE_NAME}_CNNannotated.vcf" \
   --resource "$VARIANT_DIR/hapmap_3.3.hg38.vcf.gz" \
   --resource "$VARIANT_DIR/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz" \
   --info-key CNN_2D \
   --snp-tranche 99.95 \
   --indel-tranche 99.4 \
   --invalidate-previous-filters \
   -O "$DATA_DIR/${FULL_SAMPLE_NAME}_filtervarianttranches.vcf"
 ```
### Step 8: annotatedbSNP
- Purpose: annotates variants with known variants IDs from dbSNP.
- Input: VCF
- Output: annotated VCF
```
gatk VariantAnnotator \
    -V "$DATA_DIR/${FULL_SAMPLE_NAME}_filtervarianttranches.vcf" \
    -reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
    -O "$DATA_DIR/${FULL_SAMPLE_NAME}_annotateID.vcf" \
    -dbsnp "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"
 ```
 ### Step 9: funcotator
- Purpose: annotates variants based on known (gnomAD) datasets.
- Input: VCF
- Output: annotated VCF
```
gatk Funcotator \
     --variant "$DATA_DIR/${FULL_SAMPLE_NAME}_annotateID.vcf" \
     --reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
     --ref-version hg38 \
     --data-sources-path "$gnomAD_DIR/" \
     --output "$DATA_DIR/${FULL_SAMPLE_NAME}_funcotator.vcf" \
     --output-file-format VCF
 ```
 ### Step 10: splitVCF
- Purpose: split VCF into separate SNP and INDEL files. 
- Also adding dbsnp annotations which should have been added in haplotypecaller step.
```
gatk SplitVcfs \
 -I "$DATA_DIR/${FULL_SAMPLE_NAME}_funcotator.vcf" \
 -SNP_OUTPUT "$DATA_DIR/${FULL_SAMPLE_NAME}_func_splitSNP.vcf" \
 -INDEL_OUTPUT "$DATA_DIR/${FULL_SAMPLE_NAME}_func_splitINDEL.vcf" \
 -STRICT false
 ```

 ### Remaining analysis steps will be performed in python (work in progress) 

 ### References:
 - Workflow overview: https://gatk.broadinstitute.org/hc/en-us/articles/360035535912-Data-pre-processing-for-variant-discovery
 - Generating ubam from fastq: https://gatk.broadinstitute.org/hc/en-us/articles/4403687183515--How-to-Generate-an-unmapped-BAM-from-FASTQ-or-aligned-BAM
 - Pre-processing guide: https://gatk.broadinstitute.org/hc/en-us/articles/360039568932--How-to-Map-and-clean-up-short-read-sequence-data-efficiently
 - Variant calling guide: https://gatk.broadinstitute.org/hc/en-us/articles/360035535932-Germline-short-variant-discovery-SNPs-Indels