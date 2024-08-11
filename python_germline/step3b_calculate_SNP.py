import pandas as pd

#Dataset = "/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_concat-TiTv.csv"
Dataset = "/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_filtered.csv"

df = pd.read_csv(Dataset)

dbSNP_classification = []

# for loop to see if there is a value in the ID column
# intially checked for value but returned all as 100% so switched to NaN (missing value)
#     if df.loc[i, 'ID']:

for i in range(len(df)):
    if pd.notna(df.loc[i, 'ID']):
        dbSNP_classification.append('Yes')
    else:
        dbSNP_classification.append('No')

df['dbSNP'] = dbSNP_classification

dbSNP_count = dbSNP_classification.count('Yes')
No_dbSNP_count = dbSNP_classification.count('No')

percent_dbSNP = (dbSNP_count / (dbSNP_count + No_dbSNP_count)) * 100

print("The number of variants with dbSNP IDs is", dbSNP_count)
print("The number of variants without dbSNP IDs is", No_dbSNP_count)

print(percent_dbSNP,"% of variants have dnSNP IDs")

#df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_TiTv_dbSNP.csv', index=False)
df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_dbSNP.csv', index=False)
