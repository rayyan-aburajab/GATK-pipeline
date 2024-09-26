import re

VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/SV_analysis/Manta_exome/results/variants/somaticSV.vcf'
output_file = '/coh_labs/dits/rayyan/Data/C083-000002/SV_analysis/Manta_exome/results/variants/somaticSV_filtered.vcf'

Meta_data = []
VCF_data = []

pass_pattern = re.compile(r'PASS')

with open(VCF_file, 'r') as VCF:
    for line in VCF:
        if line.startswith('#'):
            Meta_data.append(line)
            continue
        
        if pass_pattern.search(line.strip()):
            VCF_data.append(line.strip() + '\n')

combined_data = Meta_data + VCF_data

with open(output_file, 'w') as output_file:
    for record in combined_data:
        output_file.write(record)