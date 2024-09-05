import re

# VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.clinvar.vcf'
# output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.refilter.vcf'

# Meta_data = []
# VCF_data = []

# VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
# info_pattern = re.compile(r'(\w+)=?([^;]*)')

# headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

# with open(VCF_file, 'r') as VCF:
#     for line in VCF:
#         if line.startswith('#'):
#             Meta_data.append(line)
#             continue
        
#         match = VCF_pattern.match(line.strip())
#         if match:
#             record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}

#             info_dict = dict(info_pattern.findall(record_dict['INFO']))
#             record_dict['INFO'] = info_dict
#         
#         if (
#                 record_dict['FILTER'] == 'PASS' and 
#                 float(info_dict.get('SomaticEVS', '0')) >= 10.0 and
#                 float(info_dict.get('MQ', '0')) >= 40.0 and
#                 float(info_dict.get('QSS', '0')) >= 50.0
#             ):
#                 VCF_data.append(line.strip() + '\n')

# combined_data = Meta_data + VCF_data

# with open(output_file, 'w') as output_file:
#     for record in combined_data:
#         output_file.write(record)


#INDELS
VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.indels.clinvar.vcf'
output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.indels.filtered2.vcf'

Meta_data = []
VCF_data = []

VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=?([^;]*)')

headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

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
        
        if (
                record_dict['FILTER'] == 'PASS' and
                float(info_dict.get('SomaticEVS', '0')) >= 10.0 and
                float(info_dict.get('MQ', '0')) >= 40.0 and
                float(info_dict.get('QSI', '0')) >= 20
            ):
            VCF_data.append(line.strip() + '\n')

combined_data = Meta_data + VCF_data

with open(output_file, 'w') as output_file:
    for record in combined_data:
        output_file.write(record)

