import re

clinvar_vcf = "/coh_labs/dits/rayyan/References/ClinVar/clinvar.vcf"

#SNP
data_vcf = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_reformat.vcf'
output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_clinvar.vcf'

#indel
# data_vcf = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_reformat.vcf'
# output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_clinvar.vcf'

clinvar_pattern = re.compile(r'^(\d+)\t(\d+)\t(.*?)\t(\w+)\t(\w+)\t(.*?)\t(.*?)\t(.*)')
data_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=?([^;]*)')

clinvar_headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
data_headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']

clinvar_dict = {}
clinvar_key_names = set()

with open(clinvar_vcf, 'r') as clinvar:
    for line in clinvar:
        if line.startswith('#'):
            continue
        clinvar_match = clinvar_pattern.match(line.strip())
        if clinvar_match:
            clinvar_record_dict = {clinvar_headers[i]: clinvar_match.group(i + 1) for i in range(len(clinvar_headers))}
            clinvar_key = f"{'chr' + clinvar_record_dict['CHROM']}:{clinvar_record_dict['POS']}:{clinvar_record_dict['REF']}:{clinvar_record_dict['ALT']}"
            clinvar_info_dict = {f"ClinVar_VCF_{k}": v for k, v in info_pattern.findall(clinvar_record_dict['INFO'])}
            clinvar_dict[clinvar_key] = clinvar_info_dict
            clinvar_key_names.update(clinvar_info_dict.keys())

with open(data_vcf, 'r') as VCF, open(output_file, 'w') as out:
    for line in VCF:
        if line.startswith('#'):
            out.write(line)
            continue
        
        data_match = data_pattern.match(line.strip())
        if data_match:
            data_record_dict = {data_headers[i]: data_match.group(i + 1) for i in range(len(data_headers))}
            data_key = f"{data_record_dict['CHROM']}:{data_record_dict['POS']}:{data_record_dict['REF']}:{data_record_dict['ALT']}"
            
            data_info_dict = dict(info_pattern.findall(data_record_dict['INFO']))
            
            data_info_dict = {k: v for k, v in data_info_dict.items() if not k.startswith('ClinVar_VCF_') or v}
            
            if data_key in clinvar_dict:
                data_info_dict.update(clinvar_dict[data_key])
            else:
                for key in clinvar_key_names:
                    data_info_dict[key] = ''

            data_record_dict['INFO'] = ";".join([f"{k}={v}" for k, v in data_info_dict.items()])

            updated_line = "\t".join([data_record_dict[header] for header in data_headers]) + "\n"
            out.write(updated_line)