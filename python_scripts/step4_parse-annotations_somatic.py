import re

SAMPLE_NAME = input("Enter the sample name: ")
variant_type = input("Enter the variant type you are looking for (LOF or Pathogenic): ").strip().upper()

VCF_SNP_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_TumorDNA/{SAMPLE_NAME}_TumorDNA_somatic.snvs.clinvar.vcf'
VCF_INDEL_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_TumorDNA/{SAMPLE_NAME}_TumorDNA_somatic.indels.clinvar.vcf'

output_txt_file = f'/coh_labs/dits/rayyan/Data/{SAMPLE_NAME}/PythonAnalysis_TumorDNA/{SAMPLE_NAME}_somatic_variant_results.txt'

pathogenic_pattern = re.compile(r'pathogenic', re.IGNORECASE)
vcf_pattern = re.compile(r'^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
info_pattern = re.compile(r'(\w+)=([^;]*)')

headers = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR']

lof_snp_variants = ["NONSENSE", "NONSTOP", "START_CODON_SNP", "DE_NOVO_START_OUT_FRAME", "DE_NOVO_START_IN_FRAME"]
lof_indel_variants = ["START_CODON_INS", "START_CODON_DEL", "FRAME_SHIFT_INS", "FRAME_SHIFT_DEL", "DE_NOVO_START_IN_FRAME", "DE_NOVO_START_OUT_FRAME"]

with open(output_txt_file, 'w') as file:

    def parse_pathogenic_variant(info_dict, record_dict):
        if any(pathogenic_pattern.search(value) for value in info_dict.values()):
            file.write(f"Pathogenic Variant: \n")
            file.write(f"CHROM: {record_dict['CHROM']}, POS: {record_dict['POS']}, ID: {record_dict['ID']}\n")
            file.write(f"Gencode_43_hugoSymbol: {info_dict.get('Gencode_43_hugoSymbol', '')}\n")
            file.write(f"ClinVar Clinical Significance: {info_dict.get('ClinVar_VCF_CLNSIG', '')}\n")
            file.write(f"ClinVar Conflicting Clinical Significance: {info_dict.get('ClinVar_VCF_CLNSIGCONF', '')}\n")
            file.write(f"ClinVar Clinical Disease Name: {info_dict.get('ClinVar_VCF_CLNDN', '')}\n\n")

    def parse_lof_variant(info_dict, record_dict):
        if (info_dict.get("Gencode_43_variantClassification") in lof_snp_variants or
           info_dict.get("Gencode_43_secondaryVariantClassification") in lof_snp_variants or
           info_dict.get("Gencode_43_variantClassification") in lof_indel_variants or
           info_dict.get("Gencode_43_secondaryVariantClassification") in lof_indel_variants):
                file.write(f"Possible Loss of Function Variant: \n")
                file.write(f"CHROM: {record_dict['CHROM']}, POS: {record_dict['POS']}, ID: {record_dict['ID']}\n") 
                file.write(f"Gene Symbol: {info_dict.get('Gencode_43_hugoSymbol', '')}\n")
                file.write(f"Variant Classification: {info_dict.get('Gencode_43_variantClassification', '')}\n")
                file.write(f"Secondary Variant Classification: {info_dict.get('Gencode_43_secondaryVariantClassification', '')}\n")
                file.write(f"Protein Change: {info_dict.get('Gencode_43_proteinChange', '')}\n")
                file.write(f"ClinVar Clinical Significance: {info_dict.get('ClinVar_VCF_CLNSIG', '')}\n\n")

    for annotated_VCF in [VCF_SNP_file, VCF_INDEL_file]:
        with open(annotated_VCF, 'r') as vcf:
            for line in vcf:
                if line.startswith('#'):
                    continue
                
                match = vcf_pattern.match(line.strip())
                if match:
                    record_dict = {headers[i]: match.group(i + 1) for i in range(len(headers))}
                    info_dict = dict(info_pattern.findall(record_dict['INFO']))

                    if variant_type == "LOF":
                        parse_lof_variant(info_dict, record_dict)
                            
                    elif variant_type == "PATHOGENIC":
                        parse_pathogenic_variant(info_dict, record_dict)

print(f"Results have been written to {output_txt_file}.")
