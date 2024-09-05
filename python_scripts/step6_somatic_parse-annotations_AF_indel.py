import re

VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.indels.clinvar.vcf'
output = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.indels.AF-filter.vcf'

data_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
data_headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

with open(VCF_file, 'r') as VCF, open(output, 'w') as out:
    for line in VCF:
        if line.startswith('#'):
            continue
        
        data_match = data_pattern.match(line.strip())
        if data_match:
            record_dict = {data_headers[i]: data_match.group(i + 1) for i in range(len(data_headers))}
            format_keys = record_dict['FORMAT'].split(':')
            normal_values = record_dict['NORMAL'].split(':')
            tumor_values = record_dict['TUMOR'].split(':')
            record_dict['NORMAL'] = dict(zip(format_keys, normal_values))
            record_dict['TUMOR'] = dict(zip(format_keys, tumor_values))

            REF_count = int(record_dict['TUMOR'].get('TAR', '0').split(',')[0])
            ALT_count = int(record_dict['TUMOR'].get('TIR', '0').split(',')[0])
            other_count = int(record_dict['TUMOR'].get('TOR', '0').split(',')[0])

            
            
            ALT_AF = ALT_count / (ALT_count + REF_count + other_count)

            if ALT_AF > 0.1:
                out.write(line)
                print("Variant allele frequency is" + str(ALT_AF))





