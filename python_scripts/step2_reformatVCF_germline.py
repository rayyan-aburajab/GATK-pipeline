import re

SAMPLE_NAME = input("Enter the sample name: ")
SAMPLE_TYPE = "GermlineDNA"

VCF_SNP_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_SNP_filtered.vcf'
VCF_INDEL_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_INDEL_filtered.vcf'

output_SNP_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_SNP_reformat.vcf'
output_INDEL_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_GermlineDNA/{SAMPLE_NAME}_GermlineDNA_INDEL_reformat.vcf'

VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=?([^;]*)')

headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']

funcotation_header_regex = re.compile(r'##INFO=<ID=FUNCOTATION,.*?Funcotation fields are: (.*?)">')
funcotation_headers = []

def process_vcf(VCF_file, output_file, variant_type):
    global funcotation_headers

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


process_vcf(VCF_SNP_file, output_SNP_file, variant_type='SNP')

process_vcf(VCF_INDEL_file, output_INDEL_file, variant_type='INDEL')