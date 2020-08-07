Output Files are categorized as follows:


  Unmatched_____.fastq = R1 (Forward) or R4 (Reverse) reads(with barcode information appended to the headerlines) that demonstrate index hopping with barcodes that have an average Qscore above 30
  
  
  Unknown_______.fastq = R1 (Forward) or R4 (Reverse) reads with an average index Qscore less than 30 OR an "N" base is called in either the R2 or R3 sequences.
  
  
  StatsFile.fastq = Statistics collected on all files.
  
  
  Output Files by Index: Files are named with the information associated with the sequence from indexes.txt.
    
    
    Format: (sample)_(group)_(treatment)_(index)___REVERSE_S1_L008_R4_001.fastq.gz
    
    
    Example: 10_2G_both_C4___FORWARD_S1_L008_R1_001.fastq.gz is from Sample 10, Group 2G, Treatment both, and index C4.
    

StatsFile.fastq will contain stats on all FASTQ files generated. Statistics generated: Total Number of Reads, Total Amount of Index Hopping, Total Amount of Unknown Reads, Total 

Amount of Matched, Known Reads, and Percentages of each set of barcode combinations possible given indexes.txt
