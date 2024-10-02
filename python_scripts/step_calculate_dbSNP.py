import sys
import re

SNP = input("SNP prompt")
SNP_file = open(SNP)
SNP_file_components = SNP_file.readlines()

pattern_dbSNP = re.compile(r'\trs\d+')


SNP_yes = 0
SNP_no = 0

for lines in SNP_file_components:
    if lines.startswith('#'):
        continue
    else:
        if pattern_dbSNP.search(lines):
            SNP_yes +=1
        else:
            SNP_no +=1

SNP_percent_dbSNP = (SNP_yes / float(SNP_yes + SNP_no)) * 100

print("The number of SNP variants with dbSNP IDs is", SNP_yes)
print ("The number of SNP variants without dbSNP IDs is", SNP_no)
print (SNP_percent_dbSNP,"% of SNP variants have dbSNP IDs")

#####

indel = input("INDEL prompt")
indel_file = open(indel)
indel_file_components = indel_file.readlines()

pattern_dbSNP = re.compile(r'\trs\d+')

indel_yes = 0
indel_no = 0

for lines in indel_file_components:
    if lines.startswith('#'):
        continue
    else:
        if pattern_dbSNP.search(lines):
            indel_yes +=1
        else:
            indel_no +=1

indel_percent_dbSNP = (indel_yes / float(indel_yes + indel_no)) * 100

print("The number of indel variants with dbSNP IDs is", indel_yes)
print ("The number of indel variants without dbSNP IDs is", indel_no)
print (indel_percent_dbSNP,"% of indel variants have dbSNP IDs")