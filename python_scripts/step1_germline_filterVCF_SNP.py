import re

VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/AnalysisData_germline/C083-000002_GermlineDNA_func_splitSNP-dbsnp.vcf'

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
combined_data = Meta_data + VCF_data

output_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_filtered.vcf'

with open(output_VCF, 'w') as output_file:
    for record in combined_data:
        output_file.write(record)