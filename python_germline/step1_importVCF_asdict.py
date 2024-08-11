import pandas as pd
import vcf

#Read VCF
#SNP_VCF = "/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_func_splitSNP-dbsnp.vcf"
INDEL_VCF = "/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_func_splitINDEL-dbsnp.vcf"

#vcf_reader = vcf.Reader(open(SNP_VCF, 'r'))
vcf_reader = vcf.Reader(open(INDEL_VCF, 'r'))

#creating an empty list
vcf_data = []

#separate metadata fields
    #keeping "FUNCOTATION" as one for now
    #breaking up "INFO" (record.info.get) and "GENOTYPE" (record.genotype)
    #change empty "FILTER" entries to PASS 

for record in vcf_reader:
    vcf_record = {
        'CHROM': record.CHROM,
        'POS': record.POS,
        'ID': record.ID,
        'REF': record.REF,
        'ALT': record.ALT,
        'QUAL': record.QUAL,
        'FILTER': record.FILTER[0] if record.FILTER else 'PASS',
        'AC': record.INFO.get('AC', None),
        'AF': record.INFO.get('AF', None),
        'AN': record.INFO.get('AN', None),
        'BaseQRankSum': record.INFO.get('BaseQRankSum', None),
        'CNN_2D': record.INFO.get('CNN_2D', None),
        'DB': record.INFO.get('DB', None),
        'DP': record.INFO.get('DP', None),
        'ExcessHet': record.INFO.get('ExcessHet', None),
        'FS': record.INFO.get('FS', None),
        'FUNCOTATION': record.INFO.get('FUNCOTATION', None),
        'InbreedingCoeff': record.INFO.get('InbreedingCoeff', None),
        'MLEAC': record.INFO.get('MLEAC', None),
        'MLEAF': record.INFO.get('MLEAF', None),
        'MQ': record.INFO.get('MQ', None),
        'MQRankSum': record.INFO.get('MQRankSum', None),
        'QD': record.INFO.get('QD', None),
        'ReadPosRankSum': record.INFO.get('ReadPosRankSum', None),
        'SOR': record.INFO.get('SOR', None),
        'Genotype.GT': record.genotype('C083-000002_GermlineDNA').data.GT if record.genotype('C083-000002_GermlineDNA') else None,
        'Genotype.AD': record.genotype('C083-000002_GermlineDNA').data.AD if record.genotype('C083-000002_GermlineDNA') else None,
        'Genotype.DP': record.genotype('C083-000002_GermlineDNA').data.DP if record.genotype('C083-000002_GermlineDNA') else None,
        'Genotype.GQ': record.genotype('C083-000002_GermlineDNA').data.GQ if record.genotype('C083-000002_GermlineDNA') else None,
        'Genotype.PL': record.genotype('C083-000002_GermlineDNA').data.PL if record.genotype('C083-000002_GermlineDNA') else None
    }

    vcf_data.append(vcf_record)

df_vcf = pd.DataFrame(vcf_data)


# if theres multiple filters need to use semicolon to join them into a string:
    # ';'.join(record.FILTER) if record.FILTER else 'PASS'


print(df_vcf.head())

#df_vcf.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_fulldata_asdict.csv', index=False)
df_vcf.to_csv('/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_fulldata_asdict.csv', index=False)