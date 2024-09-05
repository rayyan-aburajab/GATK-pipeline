import re

VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.refilter.vcf'
output_file1 = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.remove-germ-alleles.vcf'
output_file2 = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.removed-alleles.vcf'

data_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
data_headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

with open(VCF_file, 'r') as VCF, open(output_file1, 'w') as out1, open(output_file2, 'w') as out2:
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

            if (record_dict['ALT'] == "A" and record_dict['NORMAL'].get("AU") == "0,0" or 
                record_dict['ALT'] == "T" and record_dict['NORMAL'].get("TU") == "0,0" or 
                record_dict['ALT'] == "C" and record_dict['NORMAL'].get("CU") == "0,0" or 
                record_dict['ALT'] == "G" and record_dict['NORMAL'].get("GU") == "0,0"):
                out1.write(line)
            else:
                out2.write(line)



