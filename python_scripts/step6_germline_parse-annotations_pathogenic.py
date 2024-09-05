import re

#GERMLINE
# annotated_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_clinvar.vcf'
annotated_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_clinvar.vcf'

vcf_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=([^;]*)')
pathogenic_pattern = re.compile(r'Pathogenic|Likely_pathogenic')


headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']

with open(annotated_VCF, 'r') as vcf:
#with open(annotated_VCF, 'r') as vcf, open(output_file, 'w') as out:
    for line in vcf:
        if line.startswith('#'):
            continue
        
        match = vcf_pattern.match(line.strip())
        if match:
            record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}
            info_dict = dict(info_pattern.findall(record_dict['INFO']))
            
            if any(pathogenic_pattern.search(value) for value in info_dict.values()):
                print("Pathogenic Variant:")
                print("CHROM:", record_dict['CHROM'])
                print("POS:", record_dict['POS'])
                print("ID:", record_dict['ID'])
                print("Gencode_43_hugoSymbol: " + info_dict.get('Gencode_43_hugoSymbol', ''))
                print("ClinVar Clinical Significance: " + info_dict.get('ClinVar_VCF_CLNSIG', ''))
                print("ClinVar Conflicting Clinical Significance: " + info_dict.get('ClinVar_VCF_CLNSIGCONF', ''))
                print("ClinVar Clinical Disease Name: " + info_dict.get('ClinVar_VCF_CLNDN', ''))
                print('')
