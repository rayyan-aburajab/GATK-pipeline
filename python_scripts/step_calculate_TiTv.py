import sys
import re

SNP = input("prompt")
SNP_file = open(SNP)
SNP_file_components = SNP_file.readlines()
                            
pattern_transitions = re.compile(r'\tA\tG|\tG\tA|\tC\tT|\tT\tC')
pattern_transversions =re.compile(r'\tA\tT|\tT\tA|\tA\tC|\tC\tA|\tG\tT|\tT\tG|\tG\tC|\tC\tG')

pattern_transitions_multi = re.compile(r'\tA\t[^\t],G|\tG\t[^\t],A|\tC\t[^\t],T|\tT\t[^\t],C')
pattern_transversions_multi = re.compile(r'\tA\t[^\t],T|\tT\t[^\t],A|\tA\t[^\t],C|\tC\t[^\t],A|\tG\t[^\t],T|\tT\t[^\t],G|\tG\t[^\t],C|\tC\t[^\t],G')


transition = 0
transversion = 0
unclear = 0

for lines in SNP_file_components:
    if lines.startswith('#'):
        continue
    elif pattern_transitions.search(lines) or pattern_transitions_multi.search(lines):
        transition +=1
    elif pattern_transversions.search(lines) or pattern_transversions_multi.search(lines):
        transversion +=1
    else:
        unclear +=1

ti_tv_ratio = transition / float(transversion)


print("The number of transitions is", transition)
print ("The number of transversions is", transversion)
print ("The number of SNPs that are unclear is", unclear)
print ("The Ti/Tv ratio is", ti_tv_ratio)