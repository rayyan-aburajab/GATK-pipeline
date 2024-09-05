import re

#GERMLINE
annotated_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_clinvar.vcf'
output = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_AF-filter.vcf'

# annotated_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_clinvar.vcf'
# output = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_AF-filter.vcf'

vcf_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=([^;]*)')

headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']

with open(annotated_VCF, 'r') as vcf, open(output, 'w') as out:
    for line in vcf:
        if line.startswith('#'):
            continue
        
        match = vcf_pattern.match(line.strip())
        if match:
            record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}

            format_keys = record_dict['FORMAT'].split(':')
            values = record_dict['SAMPLE'].split(':')
            record_dict['SAMPLE'] = dict(zip(format_keys, values))

            AD_values = record_dict['SAMPLE'].get('AD', '0,0').split(',')
            REF_count = int(AD_values[0])
            ALT_count = int(AD_values[1])
            DP = int(record_dict['SAMPLE'].get('DP'))

            ALT_AF = ALT_count / DP

            if ALT_AF > 0.9:
                out.write(line)


