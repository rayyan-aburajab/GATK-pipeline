import pandas as pd
import vcf

#Read VCF
#SNP_VCF = "/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_func_splitSNP-dbsnp.vcf"
INDEL_VCF = "/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_func_splitINDEL-dbsnp.vcf"

#vcf_reader = vcf.Reader(open(SNP_VCF, 'r'))
vcf_reader = vcf.Reader(open(INDEL_VCF, 'r'))


vcf_data = []

#separate metadata fields (keeping funcotator as one for now, breaking up "INFO" and "GENOTYPE")
for record in vcf_reader:
    vcf_record = [
        record.CHROM, record.POS, record.ID, record.REF, record.ALT, record.QUAL, 
        ';'.join(record.FILTER) if record.FILTER else 'PASS',
        record.INFO.get('AC', None), record.INFO.get('AF', None), record.INFO.get('AN', None),
        record.INFO.get('BaseQRankSum', None), record.INFO.get('CNN_2D', None), 
        record.INFO.get('DB', None), record.INFO.get('DP', None),
        record.INFO.get('ExcessHet', None), record.INFO.get('FS', None), record.INFO.get('FUNCOTATION', None),
        record.INFO.get('InbreedingCoeff', None), record.INFO.get('MLEAC', None), record.INFO.get('MLEAF', None),
        record.INFO.get('MQ', None), record.INFO.get('MQRankSum', None), record.INFO.get('QD', None),
        record.INFO.get('ReadPosRankSum', None), record.INFO.get('SOR', None),
        record.genotype('C083-000002_GermlineDNA').data.GT,
        record.genotype('C083-000002_GermlineDNA').data.AD,
        record.genotype('C083-000002_GermlineDNA').data.DP,
        record.genotype('C083-000002_GermlineDNA').data.GQ,
        record.genotype('C083-000002_GermlineDNA').data.PL
    ]

    vcf_data.append(vcf_record)

columns = [
    'CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'AC', 'AF', 'AN', 'BaseQRankSum', 'CNN_2D', 'DB', 'DP', 'ExcessHet',
    'FS', 'FUNCOTATION', 'InbreedingCoeff', 'MLEAC', 'MLEAF', 'MQ', 'MQRankSum', 'QD', 'ReadPosRankSum', 'SOR',
    'Genotype.GT', 'Genotype.AD', 'Genotype.DP', 'Genotype.GQ', 'Genotype.PL'
]

df_vcf = pd.DataFrame(vcf_data, columns=columns)

print(df_vcf.head())

df_vcf.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythoAnalysis_germline/C083-000002_GermlineDNA_SNP_full-dataset.csv', index=False)