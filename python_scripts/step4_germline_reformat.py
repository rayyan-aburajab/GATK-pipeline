import re

#SNP
# VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_filtered.vcf'
# output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_reformat.vcf'

#INDEL
VCF_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_filtered.vcf'
output_file = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_reformat.vcf'

VCF_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=?([^;]*)')

headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']

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


                #if funcotation_dict.get("Gencode_43_proteinChange"):
                #if funcotation_dict.get("ClinVar_VCF_CLNSIG"):
                # if funcotation_dict.get("Gencode_43_variantClassification") == "NONSENSE" or funcotation_dict.get("Gencode_43_secondaryVariantClassification") == "NONSENSE":
                # if funcotation_dict.get("Gencode_43_proteinChange"):
                    #print("Variant with protein change found:")
                    # print("CHROM:", record_dict['CHROM'])
                    # print("POS:", record_dict['POS'])
                    # print("ID:", record_dict['ID'])
                    # print("Gencode_43_hugoSymbol: " + funcotation_dict.get('Gencode_43_hugoSymbol', ''))
                    # print("Variant Classification: " + funcotation_dict.get('Gencode_43_variantClassification', ''))
                    # print("Disease Name:", funcotation_dict.get("ACMG_recommendation_Disease_Name"))
                    #out.write(line)
                    # out.write(str(record_dict) + '\n')
                    