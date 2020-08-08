I have two sets of results listed in /home/mchang3/bgmp/bioinformatics/Bi622:
One set of files is located in the directory "alternatefile". This set of files is coded with the average phred score of R2 and R3 indexes above 30.
The other set of files is located in "coveragecutoff20". This set of files is coded to put all files with any index phred scores below 20 in R2 or R3 sorted to unknown.
I've uploaded both Stats files (as labeled). Overall, I prefer the Average Phred score method since it sorts fewer to Unknown and provides a high degree of confidence.


Output Files are categorized as follows:

UNMATCHED_OUTPUT_FILES contains:

  Unmatched_____.fastq = R1 (Forward) or R4 (Reverse) reads(with barcode information appended to the headerlines) that demonstrate index hopping with barcodes that have an average Qscore above 30
  
UNKNOWN_OUTPUT_FILES contains:
  Unknown_______.fastq = R1 (Forward) or R4 (Reverse) reads with an average index Qscore less than 30 OR an "N" base is called in either the R2 or R3 sequences.
  
  
StatsFile.fastq = Statistics collected on all files.
  
INDEX_OUTPUT_FILES contains  
  Output Files by Index: Files are named with the information associated with the sequence from indexes.txt.
    
    Format: (sample)_(group)_(treatment)_(index)___REVERSE_S1_L008_R4_001.fastq.gz
    
    Example: 10_2G_both_C4___FORWARD_S1_L008_R1_001.fastq.gz is from Sample 10, Group 2G, Treatment both, and index C4.
    

StatsFile.fastq will contain stats on all FASTQ files generated. Statistics generated: Total Number of Reads, Total Amount of Index Hopping, Total Amount of Unknown Reads, Total 

Amount of Matched, Known Reads, and Percentages of each set of barcode combinations possible given indexes.txt
