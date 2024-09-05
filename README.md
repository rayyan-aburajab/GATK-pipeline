# GATK-Pipeline
## Germline Variant Analysis
#### GATK Best Practices Pipeline:
See details in [Germline Subdirectory](GATK_germline/README.md)

Pre-processing:
- Step 1: convert fastq files to unmapped bam (ubam) format
- Step 2: mark illumina adapters
- Step 3a: convert ubam back to fastq format
- Step 3b: align using bwa-mem
- Step 3c: merge mapped and unmapped bam files
- Step 4: mark duplicate reads
- Step 5: (skip in this workflow)

Variant calling:
- Step 6: determine haplotypes and assign genotypes 
- Step 7: score and annotate variant quality
- Step 8: filter variants based on scores
- Step 9: funcotator annotations
- Step 10: split VCF into SNP and INDEL

## Somatic Variant Analysis
See details in [Somatic Subdirectory](GATK_Strelka_somatic/README.md)

#### GATK Pre-Processing

- Step 1: convert fastq files to unmapped bam (ubam) format
- Step 2: mark illumina adapters
- Step 3a: convert ubam back to fastq format
- Step 3b: align using bwa-mem
- Step 3c: merge mapped and unmapped bam files
- Step 4: mark duplicate reads

#### Strelka2 Variant Calling

- Step 5a: configure Strelka workflow
- Step 5b: execute Strelka variant calling workflow

#### GATK Post-Processing

- Step 6: (python filtering - to be changed)
- Step 7: funcotator annotations
- Step 8: add dbSNP IDs

## Python Analysis

See details in [Python Subdirectory](python_scripts/README.md)

- Manual filtering VCF files
- Reformat Funcotator annotations
- Add ClinVar annotations (due to Funcotator error)
- Parse VCF files (eg. LOF, pathogenic variants, allele frequencies)
- Calculate % of variants with dbSNP IDs
- Calculate Ti/Tv ratio