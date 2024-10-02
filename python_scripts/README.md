# Processing VCF Files with Python

##### These scripts are designed to filter, annotate, and parse germline and somatic (tumor) VCF files

These steps begin from the outputs of:
- Step 10 in the germline workflow
- Step 7b in the somatic workflow

*Note 10/2/24: script has been modified to take sample names as user input*

## Step 1: Filtering

- Purpose: Perform further quality filtering on variants that passed default GATK/Strelka filtering criteria.
- Script summary: Define REGEX pattern for VCF fields to create RECORD dictionary. Define REGEX pattern for INFO field to create INFO dictionary.

##### Germline filters:
- SNP: QUAL ≥ 50, QD ≥ 2, SOR ≤ 3 , FS ≤ 60, MQ ≥ 40, MQRankSum ≥ -12.5, ReadPosRankSum ≥ -8, GQ ≥ 99
- Indel: QUAL ≥ 50, QD ≥ 2, FS ≤ 200, ReadPosRankSum ≥ -20, GQ ≥ 99

##### Somatic filters:
- SNP: SomaticEVS ≥ 50, MQ ≥ 40, QSS ≥ 50
- Indel: SomaticEVS ≥ 10, MQ ≥ 40

## Step 2: Reformatting

- Purpose: Funcotator annotations are populated as a single pipe-separated string (k= [v|v|v]) within a key-value pair in the INFO field. Therefore, this script converts funcotator annotations from piped (v|v|v) format to key-value pair (k=v; k=v; k=v) format. 
- Script summary: Create RECORD/INFO dictionaries as in Step 1. Define REGEX pattern for FUNCOTATION annotation to create FUNCOTATION dictionary and join to INFO dictionary.

## Step 3: ClinVar Annotations

- Purpose: Funcotator annotation contains faulty (missing) ClinVar entries. Therefore, this script repopulates the VCFs with the correct/complete annotations using ClinVar short variant database (provided in VCF format - https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/).

- Script summary: Create RECORD/INFO dictionaries as in Step 1. Create key-value pairs where CHROM:POS:REF:ALT fields serve as key and INFO dictionary serves as value for both the ClinVar database VCF and sample VCF file. The script will then match keys from the sample VCF file to the ClinVar database VCF and join values to the INFO dictionary (pre-existing ClinVar annotations will be removed).

## Step 4: Parse Annotations

- Purpose: Design script to parse through annotations for specific variant features, such as loss of function (LOF) variants and pathogenic variants. 
- LOF summary: select for primary or secondary variant classifications that could be associated with loss of function i.e. adds or removes start/stop codon or shifts reading frame and print variant identifiers, classification, protein change, and clinical significance.
- Pathogenic summary: o select for lines containing the word “pathogenic” or then print variant & additional ClinVar information.
- *Note: script can been modified to select for any additional variant features*

## Script: Calculate dbSNP

- Purpose: Calculate the percentage of variants with a known dbSNP identifier (rs_).
- Script summary: Count the number of lines containing an rs___ ID, divide by the total number lines, and print output.

## Script: Calculate TiTv

- Purpose: Calculate the ratio of SNPs that are transitions (purine-purine, pyrimidine-pyrimidine) to SNPs that are transversions (purine-pyrimidine, pyrimidine-purine).
- Script summary: Define REGEX patterns corresponding to all possible transition (Ti) and transversion (Tv) combinations. Divide the number of Ti by the number of Tv and print output.