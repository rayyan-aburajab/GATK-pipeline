import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='CNV_annotation')

# these four parameters have default values
parser.add_argument('-O', '--outpath', default='.', type=str, help='output path of the final results')
parser.add_argument('-U', '--upper', default=0.58, type=float, help='upper threshold of normal copy number. copy numbers higher than this value should be defined as copy gain')
parser.add_argument('-L', '--lower', default=-1, type=float, help='lower threshold of normal copy number. copy numbers lower than this value should be defined as copy loss')
parser.add_argument('-M', '--segmax', default=25000000, type=int, help='maximum length of segments being used')

# these three parameters do not have default value
parser.add_argument('-N', '--name', type=str, help='name of the sample')
parser.add_argument('-G', '--geneinfo', type=str, help='filename of the gene info')
parser.add_argument('-S', '--segfile', type=str, help='filename of the segment-level CNV result')

sample_name = parser.parse_args().name
upper = parser.parse_args().upper
lower = parser.parse_args().lower
seg_max = parser.parse_args().segmax
gene_info = parser.parse_args().geneinfo
seg_cnv = parser.parse_args().segfile
out_path = parser.parse_args().outpath

# read the gene info file and the segment-level CNV result file. CNV should be represented by log2 copy ratio
gene = pd.read_csv(gene_info, sep='\t', header=0)
seg = pd.read_csv(seg_cnv, sep='\t', dtype = {'Segment_Mean' : str}, header=0)
seg['Segment_Mean'] = seg['Segment_Mean'].astype(float)
gene['chrom'] = gene['chrom'].map(lambda x: 'chr' + x)
   
# read the genes one by one
for index, row in gene.iterrows():
    # create a temporary dataframe to store information of all segments that overlap with a gene
    tmp_df = seg.loc[(seg['Chromosome'] == row['chrom']) & (seg['End'] > row['start']) & (seg['Start'] < row['end'])]
    # omit genes that do not overlap with any segment
    if tmp_df.empty:
        continue
    # copy the datafram to avoid pandas warnings
    tmp_df_copy = tmp_df.copy()
    # add a column 'seg_abs' to the temporary dataframe to store the absolute value of the log2 copy ratio
    tmp_df_copy['seg_abs'] = tmp_df_copy['Segment_Mean'].abs()
    # find the index of the segment with the maximum 'seg_abs' in the temporary dataframe and store it in a variable
    abs_max_index = tmp_df_copy['seg_abs'].idxmax()
    # assign the log2 copy ratio of the segment corresponding to the index to the gene in the loop
    gene.loc[index, 'log2_copy_ratio'] = tmp_df_copy.loc[abs_max_index,'Segment_Mean']
    # if the segment length does not exceed the set maximum and the log2 copy ratio exceeds the upper threshold, mark the gene as 'gain' and store it in a new column 'loss_or_gain'
    if tmp_df_copy.loc[abs_max_index,'End'] - tmp_df_copy.loc[abs_max_index,'Start'] <= seg_max and tmp_df_copy.loc[abs_max_index,'Segment_Mean'] > upper:
        gene.loc[index, 'loss_or_gain'] = 'gain'
    # if the segment length does not exceed the set maximum and the log2 copy ratio is below the lower threshold, mark the gene as 'loss' and store it in the 'loss_or_gain' column
    elif tmp_df_copy.loc[abs_max_index,'End'] - tmp_df_copy.loc[abs_max_index,'Start'] <= seg_max and tmp_df_copy.loc[abs_max_index,'Segment_Mean'] < lower:
        gene.loc[index, 'loss_or_gain'] = 'loss'
    # define remaining genes overlapping with segments are as 'normal'
    else:
        gene.loc[index, 'loss_or_gain'] = 'normal'

# define genes that do not overlap with any segment as 'no_match'
gene.fillna(axis=0, value='no_overlap', inplace=True)
# creat a report datafram only keeping loss_or_gain column with loss and gain
gene_report = gene.drop(gene[(gene['loss_or_gain']=='normal') | (gene['loss_or_gain']=='no_overlap')].index)
# save the final dataframes
gene.to_csv(out_path + '/' + sample_name + '_annotation.txt', sep='\t', index=None)
gene_report.to_csv(out_path + '/' + sample_name + '_annotation_report.txt', sep='\t', index=None)