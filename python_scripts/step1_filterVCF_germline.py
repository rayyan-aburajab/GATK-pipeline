import re

SAMPLE_NAME = input("Enter the sample name: ")
SAMPLE_TYPE = "GermlineDNA"

VCF_SNP_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/AnalysisData_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_func_splitSNP.vcf'
VCF_INDEL_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/AnalysisData_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_func_splitINDEL.vcf'

output_SNP_VCF = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_SNP_filtered.vcf'
output_INDEL_VCF = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_INDEL_filtered.vcf'

def filter_vcf(VCF_file, output_VCF, variant_type):
    Meta_data = []
    VCF_data = []

    headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']

    VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
    info_pattern = re.compile(r'(\w+)=?([^;]*)')

    with open(VCF_file, 'r') as VCF:
        for line in VCF:
            if line.startswith('#'):
                Meta_data.append(line)
                continue
            
            match = VCF_pattern.match(line.strip())
            if match:
                record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}

                info_dict = dict(info_pattern.findall(record_dict['INFO']))
                record_dict['INFO'] = info_dict
                
                format_keys = record_dict['FORMAT'].split(':')
                sample_values = record_dict['SAMPLE'].split(':')
                sample_dict = dict(zip(format_keys, sample_values))
                record_dict['SAMPLE'] = sample_dict

            if variant_type == 'SNP':
                if (
                        record_dict['FILTER'] == 'PASS' and
                        float(info_dict.get('QD', float('-inf'))) >= 2.0 and
                        float(record_dict['QUAL']) >= 50.0 and
                        float(info_dict.get('SOR', float('inf'))) <= 3.0 and
                        float(info_dict.get('FS', float('inf'))) <= 60.0 and
                        float(info_dict.get('MQ', float('-inf'))) >= 40.0 and
                        (info_dict.get('MQRankSum') is None or float(info_dict['MQRankSum']) >= -12.5) and
                        (info_dict.get('ReadPosRankSum') is None or float(info_dict['ReadPosRankSum']) >= -8.0) and
                        float(sample_dict.get('GQ', float('-inf'))) >= 99.0
                    ):
                    VCF_data.append(line.strip() + '\n')

            elif variant_type == 'INDEL':
                if (
                        record_dict['FILTER'] == 'PASS' and
                        float(info_dict.get('QD', float('-inf'))) >= 2.0 and
                        float(record_dict['QUAL']) >= 50.0 and
                        float(info_dict.get('FS', float('inf'))) <= 200.0 and
                        float(info_dict.get('ReadPosRankSum') is None or float(info_dict['ReadPosRankSum']) >= -20.0) and
                        float(sample_dict.get('GQ', float('-inf'))) >= 99.0
                    ):
                    VCF_data.append(line.strip() + '\n')

    combined_data = Meta_data + VCF_data

    with open(output_VCF, 'w') as output_file:
        for record in combined_data:
            output_file.write(record)

    print(f"Filtered VCF saved to {output_VCF}")

filter_vcf(
    VCF_SNP_file, 
    output_SNP_VCF,
    variant_type='SNP'
)

filter_vcf(
    VCF_INDEL_file, 
    output_INDEL_VCF,
    variant_type='INDEL'
)
