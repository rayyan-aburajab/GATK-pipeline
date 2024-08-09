import pandas as pd

#dataset = "/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_SNP_full-dataset.csv"

#df_vcf = pd.read_csv(dataset)

# SNP filters QD < 2.0, QUAL < 50.0, SOR > 3.0, FS > 60.0, MQ < 40.0, genotype_GQ < 99.0, MQRankSum < -12.5, ReadPosRankSum < -8.0
# filtered_df = df_vcf[
#     (df_vcf['FILTER'] == 'PASS') &
#     (df_vcf['QD'] >= 2.0) &
#     (df_vcf['QUAL'] >= 50.0) &
#     (df_vcf['SOR'] <= 3.0) &
#     (df_vcf['FS'] <= 60.0) &
#     (df_vcf['MQ'] >= 40.0) &
#     (df_vcf['Genotype.GQ'] >= 99.0) &
#     (df_vcf['MQRankSum'] >= -12.5) &
#     (df_vcf['ReadPosRankSum'] >= -8.0)
# ]
#filtered_df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_SNP_filtered.csv', index=False)

dataset = "/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_INDEL_full-dataset.csv"
df_vcf = pd.read_csv(dataset)

# INDEL filters "QD < 2.0", "QUAL < 50.0, FS > 200.0, GQ < 99.0, ReadPosRankSum < -20.0 
filtered_df = df_vcf[
    (df_vcf['FILTER'] == 'PASS') &
    (df_vcf['QD'] >= 2.0) &
    (df_vcf['QUAL'] >= 50.0) &
    (df_vcf['FS'] <= 200.0) &
    (df_vcf['Genotype.GQ'] >= 99.0) &
    (df_vcf['ReadPosRankSum'] >= -20.0)
]
print(filtered_df.head())

filtered_df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_INDEL_filtered.csv', index=False)