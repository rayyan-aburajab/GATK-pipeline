import re

SAMPLE_NAME = input("Enter the sample name: ")
SAMPLE_TYPE = "TumorDNA"

VCF_SNP_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/AnalysisData_{SAMPLE_TYPE}/somatic.snvs.funcotator.vcf'
VCF_INDEL_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/AnalysisData_{SAMPLE_TYPE}/somatic.indels.funcotator.vcf'

output_SNP_VCF = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_{SAMPLE_TYPE}/{SAMPLE_NAME}_TumorDNA_somatic.snvs.filtered.vcf'
output_INDEL_VCF = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_{SAMPLE_TYPE}/{SAMPLE_NAME}_TumorDNA_somatic.indels.filtered.vcf'

def filter_vcf(VCF_file, output_VCF, variant_type):
    Meta_data = []
    VCF_data = []

    headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

    VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
    info_pattern = re.compile(r'(\w+)=?([^;]*)')

    with open(VCF_file, 'r', encoding='utf-8', errors='replace') as VCF:
        for line in VCF:
            if line.startswith('#'):
                Meta_data.append(line)
                continue
            
            match = VCF_pattern.match(line.strip())
            if match:
                record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}

                info_dict = dict(info_pattern.findall(record_dict['INFO']))
                record_dict['INFO'] = info_dict

            if variant_type == 'SNP':
                if (
                        record_dict['FILTER'] == 'PASS' and 
                        float(info_dict.get('SomaticEVS', '0')) >= 10.0 and
                        float(info_dict.get('MQ', '0')) >= 40.0 and
                        float(info_dict.get('QSS', '0')) >= 50.0
                    ):
                    VCF_data.append(line.strip() + '\n')

            elif variant_type == 'INDEL':
                if (
                        record_dict['FILTER'] == 'PASS' and
                        float(info_dict.get('SomaticEVS', '0')) >= 10.0 and
                        float(info_dict.get('MQ', '0')) >= 40.0
                        #float(info_dict.get('QSI', '0')) >= 20
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
