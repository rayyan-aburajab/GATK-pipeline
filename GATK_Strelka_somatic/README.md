# GATK & Strelka2 Pipeline

## Somatic (Tumor DNA)

#### GATK Version (4.6.0) - singularity container
```
module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

singularity exec "$Singularity_GATK" \
```

#### Strelka2 Version (4.6.0) - singularity container
```
module load singularity
export SINGULARITY_BIND="/coh_labs/dits/rayyan:/coh_labs/dits/rayyan"

singularity exec "$Singularity_strelka" \
```

## Part I: GATK Pre-Processing

### Step 1: fastq-to-ubam
- Purpose: Generate compatible unmapped bam input for GATK best practices workflow
- Input: Fastq (paired)
- Output: Bam (unmapped)
```
gatk FastqToSam \
 --FASTQ "$FASTQ_DIR/C083-000002_WF00054603_H036425-02D-01L_TumorDNA_R1_001.fastq.gz" \
 --FASTQ2 "$FASTQ_DIR/C083-000002_WF00054603_H036425-02D-01L_TumorDNA_R2_001.fastq.gz" \
 --OUTPUT "$OUTPUT_DIR/C083-000002_TumorDNA_fastqtosam.bam" \
 --SAMPLE_NAME C083-000002_TumorDNA
 ```
### Step 2: markadapters
- Purpose: Mark adapter sequences within reads, which arise through concatenation of adapters or readthrough of short reads
- Input: Bam (unmapped)
- Output: Bam (unmapped), metrics file
```
gatk MarkIlluminaAdapters \
 --I "$DATA_DIR/C083-000002_TumorDNA_fastqtosam.bam" \
 --O "$DATA_DIR/C083-000002_TumorDNA_markilluminaadapters.bam" \
 --M "$DATA_DIR/C083-000002_TumorDNA_markilluminaadapters_metrics.txt"
 ```
### Step 3A: ubam-to-fastq
- Purpose: Generates a fastq file (R1+2 combined) with adapter sequences removed
- Input: Bam (unmapped)
- Output: Fastq (interleaved)
```
gatk  SamToFastq \
 --I "$DATA_DIR/C083-000002_TumorDNA_markilluminaadapters.bam" \
 --FASTQ "$DATA_DIR/C083-000002_TumorDNA_samtofastq_interleaved.fq" \
 --CLIPPING_ATTRIBUTE XT --CLIPPING_ACTION 2 --INTERLEAVE true --NON_PF true 
 ```
### Step 3B: bwamem-alignment
- Purpose: Aligns sample to reference genome
- Input: Fastq (interleaved), reference
- Output: Bam (mapped)
```
bwa mem -p "$REF_DIR"/Homo_sapiens_assembly38.fasta \
"$DATA_DIR/C083-000002_TumorDNA_samtofastq_interleaved.fq" > "$DATA_DIR/C083-000002_TumorDNA_bwamem.sam"
```
Note: the linked guide recommends -M option. This is due to incompatibility between Picard and previous GATK versions. That option is no longer recommended according to more recent documentation.

### Step 3C: mergebamalignment
- Purpose: generates "clean" bam by merging aligned and unmapped bams to retain all meta data
- Input: Bam (unmapped), Bam (mapped), reference
- Output: Bam
```
gatk  MergeBamAlignment \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --ALIGNED_BAM "$DATA_DIR/C083-000002_TumorDNA_bwamem.sam" \
 --UNMAPPED_BAM "$DATA_DIR/C083-000002_TumorDNA_markilluminaadapters.bam" \
 --OUTPUT "$DATA_DIR/C083-000002_TumorDNA_mergebamalignment.bam" \
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
 --I "$DATA_DIR/C083-000002_TumorDNA_mergebamalignment.bam" \
 --O "$DATA_DIR/C083-000002_TumorDNA_markedduplicates.bam" \
 --R "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --M "$DATA_DIR/C083-000002_TumorDNA_markeddups_metrics.txt"
 ```

 ## Part II: Strelka2 Variant Calling
- Purpose: 
- Input: 
- Output: 

### Step 5a: configureStrelkaSomaticWorkflow
```
configureStrelkaSomaticWorkflow.py \
 --normalBam "$DATA_DIR_normal/C083-000002_GermlineDNA_markedduplicates.bam" \
 --tumorBam "$DATA_DIR_tumor/C083-000002_TumorDNA_markedduplicates.bam" \
 --referenceFasta "$REF_DIR/Homo_sapiens_assembly38.fasta" \
 --runDir "$DATA_DIR_tumor"
 ```
### Step 5b: runWorkflow

 ```
"$DATA_DIR_tumor/runWorkflow.py" \
 --mode local \
 --jobs 8
 ```
## Part III: GATK Post-Processing

### Step 7: Funcotator
- Purpose: annotates variants based on known datasets.
- Input: VCF
- Output: VCF
```
gatk Funcotator \
     --variant "$DATA_DIR/somatic.snvs.filtered.vcf" \
     --reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
     --ref-version hg38 \
     --data-sources-path "$gnomAD_DIR/" \
     --output "$DATA_DIR/somatic.snvs.filtered.funcotator.vcf" \
     --output-file-format VCF

gatk Funcotator \
     --variant "$DATA_DIR/somatic.indels.filtered.vcf" \
     --reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
     --ref-version hg38 \
     --data-sources-path "$gnomAD_DIR/" \
     --output "$DATA_DIR/somatic.indels.filtered.funcotator.vcf" \
     --output-file-format VCF
 ```
### Step 8: AnnotatedbSNP
- Purpose: annotates variants based on known datasets.
- Input: VCF
- Output: VCF
```
gatk VariantAnnotator \
    -V "$DATA_DIR/somatic.snvs.filtered.funcotator.vcf" \
    -reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
    -O "$DATA_DIR/somatic.snvs.filtered.funcotator-dbsnp.vcf" \
    -dbsnp "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"

gatk VariantAnnotator \
    -V "$DATA_DIR/somatic.indels.filtered.funcotator.vcf" \
    -reference "$REF_DIR/Homo_sapiens_assembly38.fasta" \
    -O "$DATA_DIR/somatic.indels.filtered.funcotator-dbsnp.vcf" \
    -dbsnp "$VARIANT_DIR/Homo_sapiens_assembly38.dbsnp138.vcf"
 ```