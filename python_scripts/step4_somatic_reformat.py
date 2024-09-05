import re

#SNP
# VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.filtered.vcf'
# output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.snvs.reformat.vcf'

#indel
VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.indels.filtered.vcf'
output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_TumorDNA/somatic.indels.reformat.vcf'

VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=?([^;]*)')

headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

funcotation_header_regex = re.compile(r'##INFO=<ID=FUNCOTATION,.*?Funcotation fields are: (.*?)">')
funcotation_headers = []

with open(VCF_file, 'r') as VCF:
    for line in VCF:
        match = funcotation_header_regex.search(line)
        if match:
            funcotation_headers = match.group(1).split('|')
            break

with open(VCF_file, 'r') as VCF, open(output_file, 'w') as out:
    for line in VCF:
        if line.startswith('#'):
            out.write(line)
            continue
        
        match = VCF_pattern.match(line.strip())
        if match:
            record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}
            info_dict = dict(info_pattern.findall(record_dict['INFO']))
            
            if 'FUNCOTATION' in info_dict:
                funcotation_values = info_dict['FUNCOTATION'].strip('[]').split('|')
                funcotation_dict = {funcotation_headers[i]: funcotation_values[i] for i in range(min(len(funcotation_headers), len(funcotation_values)))}
                
                info_dict.update(funcotation_dict)
                del info_dict['FUNCOTATION'] 

            record_dict['INFO'] = ";".join([f"{k}={v}" for k, v in info_dict.items()])

            updated_line = "\t".join([record_dict[header] for header in headers]) + "\n"
            out.write(updated_line)
                    