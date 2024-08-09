import pandas as pd

dataset1 = "/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_SNP_filtered.csv"
#dataset2 = "/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_INDEL_filtered.csv"

df1 = pd.read_csv(dataset1)
#df2 = pd.read_csv(dataset2)

if 'FUNCOTATION' in df_vcf.columns:
    # Split the FUNCOTATION column into multiple columns
    funcotator_columns = df_vcf['FUNCOTATION'].str.split('|', expand=True)