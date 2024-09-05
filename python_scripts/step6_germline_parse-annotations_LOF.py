import re

#GERMLINE
# annotated_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_SNP_clinvar.vcf'
# annotated_VCF = '/coh_labs/dits/rayyan/Data/C083-000002/PythonAnalysis_germline/C083-000002_GermlineDNA_INDEL_clinvar.vcf'

vcf_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=([^;]*)')

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
            
            #SNPs
            if (info_dict.get("Gencode_43_variantClassification") in ["NONSENSE", "NONSTOP", "START_CODON_SNP", "DE_NOVO_START_OUT_FRAME", "DE_NOVO_START_IN_FRAME"] or
                info_dict.get("Gencode_43_secondaryVariantClassification") in ["NONSENSE", "NONSTOP", "START_CODON_SNP", "DE_NOVO_START_OUT_FRAME", "DE_NOVO_START_IN_FRAME"]):
                            print("Possible Loss of Function Variant: ")
                            print("CHROM, POS, ID: ", record_dict['CHROM'], record_dict['POS'], record_dict['ID'])
                            print("Gene Symbol: " + info_dict.get('Gencode_43_hugoSymbol', ''))
                            print("Variant Classification: " + info_dict.get('Gencode_43_variantClassification', ''))
                            print("Secondary Variant Classification: " + info_dict.get('Gencode_43_secondaryVariantClassification', ''))
                            print("Protein Change: " + info_dict.get('Gencode_43_proteinChange', ''))
                            print("ClinVar Clinical Significance: " + info_dict.get('ClinVar_VCF_CLNSIG', ''))
            
            #INDELS
            if (info_dict.get("Gencode_43_variantClassification") in ["START_CODON_INS", "START_CODON_DEL", "DE_NOVO_START_IN_FRAME", "DE_NOVO_START_OUT_FRAME", "FRAME_SHIFT_INS", "FRAME_SHIFT_DEL"] or
                info_dict.get("Gencode_43_secondaryVariantClassification") in ["START_CODON_INS", "START_CODON_DEL", "DE_NOVO_START_IN_FRAME", "DE_NOVO_START_OUT_FRAME", "FRAME_SHIFT_INS", "FRAME_SHIFT_DEL"]):
                            print("Possible Loss of Function Variant: ")
                            print("CHROM, POS, ID: ", record_dict['CHROM'], record_dict['POS'], record_dict['ID'])
                            print("Gene Symbol: " + info_dict.get('Gencode_43_hugoSymbol', ''))
                            print("Variant Classification: " + info_dict.get('Gencode_43_variantClassification', ''))
                            print("Secondary Variant Classification: " + info_dict.get('Gencode_43_secondaryVariantClassification', ''))
                            print("Protein Change: " + info_dict.get('Gencode_43_proteinChange', ''))
                            print("ClinVar Clinical Significance: " + info_dict.get('ClinVar_VCF_CLNSIG', ''))

                #out.write(line)