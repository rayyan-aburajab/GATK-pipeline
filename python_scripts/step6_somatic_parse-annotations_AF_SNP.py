import re

VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.clinvar.vcf'
output = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.AF-filter.vcf'

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

            if record_dict['REF'] == "A":
                REF_count = int(record_dict['TUMOR'].get('AU', '0').split(',')[0])
            elif record_dict['REF'] == "T":
                REF_count = int(record_dict['TUMOR'].get('TU', '0').split(',')[0])                
            elif record_dict['REF'] == "C":
                REF_count = int(record_dict['TUMOR'].get('CU', '0').split(',')[0]) 
            elif record_dict['REF'] == "G":
                REF_count = int(record_dict['TUMOR'].get('GU', '0').split(',')[0])

            if record_dict['ALT'] == "A":
                ALT_count = int(record_dict['TUMOR'].get('AU', '0').split(',')[0])
            elif record_dict['ALT'] == "T":
                ALT_count = int(record_dict['TUMOR'].get('TU', '0').split(',')[0])                
            elif record_dict['ALT'] == "C":
                ALT_count = int(record_dict['TUMOR'].get('CU', '0').split(',')[0]) 
            elif record_dict['ALT'] == "G":
                ALT_count = int(record_dict['TUMOR'].get('GU', '0').split(',')[0])
            
            # DP = int(record_dict['TUMOR'].get('DP'))
            # ALT_AF = ALT_count / DP

            ALT_AF = ALT_count / (ALT_count + REF_count)

            if ALT_AF > 0.1:
                out.write(line)
                print("Variant allele frequency is " + str(ALT_AF))





