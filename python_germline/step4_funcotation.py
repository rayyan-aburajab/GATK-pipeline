import pandas as pd

Dataset = "/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_filtered.csv"
#Dataset = "/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_filtered.csv"

df = pd.read_csv(Dataset)

# df = pd.read_csv(INDEL)

# Create a dataframe from FUNCOTATION
# Remove all brackets and apostrophes
# Name cleaned up column

#want to remove some characters
    # regex below is to remove brackets and single quotes
    # r and \ are used bc [ ] are actual python symbols so we want to refer to them literally
    # So \[ = [ and \] = ]

funcotation_cleaned_df = pd.DataFrame(df['FUNCOTATION'].str.replace(r"[\[\]']", '', regex=True))
funcotation_cleaned_df.columns = ['FUNCOTATION_CLEANED']

# Split by pipe
funcotation_split = funcotation_cleaned_df['FUNCOTATION_CLEANED'].str.split('|', expand=True)

# Keep only the first 52 columns (1st set of annotation)
funcotation_52 = funcotation_split.iloc[:, :52]

# Column names from VCF
funcotation_52.columns = [
    'Gencode_43_hugoSymbol', 'Gencode_43_ncbiBuild', 'Gencode_43_chromosome',
    'Gencode_43_start', 'Gencode_43_end', 'Gencode_43_variantClassification',
    'Gencode_43_secondaryVariantClassification', 'Gencode_43_variantType',
    'Gencode_43_refAllele', 'Gencode_43_tumorSeqAllele1', 'Gencode_43_tumorSeqAllele2',
    'Gencode_43_genomeChange', 'Gencode_43_annotationTranscript',
    'Gencode_43_transcriptStrand', 'Gencode_43_transcriptExon', 'Gencode_43_transcriptPos',
    'Gencode_43_cDnaChange', 'Gencode_43_codonChange', 'Gencode_43_proteinChange',
    'Gencode_43_gcContent', 'Gencode_43_referenceContext', 'Gencode_43_otherTranscripts',
    'ACMGLMMLof_LOF_Mechanism', 'ACMGLMMLof_Mode_of_Inheritance', 'ACMGLMMLof_Notes',
    'ACMG_recommendation_Disease_Name', 'ClinVar_VCF_AF_ESP', 'ClinVar_VCF_AF_EXAC',
    'ClinVar_VCF_AF_TGP', 'ClinVar_VCF_ALLELEID', 'ClinVar_VCF_CLNDISDB',
    'ClinVar_VCF_CLNDISDBINCL', 'ClinVar_VCF_CLNDN', 'ClinVar_VCF_CLNDNINCL',
    'ClinVar_VCF_CLNHGVS', 'ClinVar_VCF_CLNREVSTAT', 'ClinVar_VCF_CLNSIG',
    'ClinVar_VCF_CLNSIGCONF', 'ClinVar_VCF_CLNSIGINCL', 'ClinVar_VCF_CLNVC',
    'ClinVar_VCF_CLNVCSO', 'ClinVar_VCF_CLNVI', 'ClinVar_VCF_DBVARID',
    'ClinVar_VCF_GENEINFO', 'ClinVar_VCF_MC', 'ClinVar_VCF_ORIGIN', 'ClinVar_VCF_RS',
    'ClinVar_VCF_ID', 'ClinVar_VCF_FILTER', 'LMMKnown_LMM_FLAGGED', 'LMMKnown_ID',
    'LMMKnown_FILTER']

# Carry over variant identity info
adddata = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL']

# Concatenate variant identity with functotation
final_df = pd.concat([df[adddata], funcotation_52], axis=1)


#print(final_df.head())

#final_df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_func.csv', index=False)
#final_df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_func.csv', index=False)