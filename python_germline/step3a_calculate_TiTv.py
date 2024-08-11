import pandas as pd

SNP = "/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_filtered.csv"
df = pd.read_csv(SNP)

# making sure that REF and ALT values are strings
# print(df.dtypes)

# types = df['ALT'].apply(type)
# print(types)

# need to remove brackets from ALT
df['ALT'] = df['ALT'].str.strip('[]')

# Transition = purine-purine (A,G) or pyrimidine-pyrimidine (C,T)
# Transversion = purine-pyrimidine interchange (A,T)(A,C)(G,T)(G,A)

transitions = {('A', 'G'), ('G', 'A'), ('C', 'T'), ('T', 'C')}
transversions = {('A', 'T'), ('T', 'A'), ('A', 'C'), ('C', 'A'), ('G', 'T'), ('T', 'G'), ('G', 'C'), ('C', 'G')}

# list to classify each entry:
ti_tv_classification = []

# for loop to go through each entry and classify as transition or tranversion
# df.loc[i, 'xxx'] is used to access the entry for each line (i) and specific column (xxx)
for i in range(len(df)):
    ref = df.loc[i, 'REF']
    alt = df.loc[i, 'ALT']
    
    if (ref, alt) in transitions:
        ti_tv_classification.append('Transition (Ti)')
    elif (ref, alt) in transversions:
        ti_tv_classification.append('Transversion (Tv)')
    else:
        ti_tv_classification.append('Other')

df['TiTv'] = ti_tv_classification

transitions_count = ti_tv_classification.count('Transition (Ti)')
transversions_count = ti_tv_classification.count('Transversion (Tv)')

ti_tv_ratio = transitions_count / transversions_count


print(df.head()) 


print("Transition (Ti) count is:", transitions_count)
print("Transversion (Tv) count is:", transversions_count)
print("TiTv ratio is:", ti_tv_ratio)

df.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_concat-TiTv.csv', index=False)
