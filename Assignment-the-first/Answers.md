# Assignment the First

## Part 1
1. Be sure to upload your Python script.

SCRIPT FOR INDEXES. SCRIPT FOR R1 AND R4 ARE THE SAME BUT ANY INSTANCE OF "8" IS REPLACED WITH 101


#!/usr/bin/env python
import argparse
import numpy as np
import gzip
def get_args():
    parser = argparse.ArgumentParser(description="Specify filename. Assumes Kmer of 49")
    parser.add_argument("-f", "--filename", help="Filename", required=True)
    parser.add_argument("-gn", "--graphname", help="Graph Name", required=True)
    return parser.parse_args()
args = get_args()
fn = args.filename
nam = args.graphname

#f = gzip.open(fn, "rt")
qscores = np.zeros(8)
LN = 0
with gzip.open(fn, "rt") as fh:
    readcounter = 0
    for line in fh:
        if LN % 4 == 3:
            nuc_pos = 0
            for i in line.strip():
                qscores[nuc_pos] += (ord(i) -33)
                nuc_pos += 1

            readcounter += 1
        LN += 1

meanqual = np.zeros((8))

for i in range(len(qscores)):
    meanqual[i] = int(qscores[i])/363246735



from matplotlib import pyplot as plt

x = [x for x in range(8)]

plt.xlabel("Nucleotide Position")
plt.ylabel("Mean Value")
plt.title("Mean Value by Position")
plt.bar(x, meanqual)
plt.savefig("{}QualScoreDist.png".format(nam))




| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz | R1 |
| 1294_S1_L008_R2_001.fastq.gz | R2 |
| 1294_S1_L008_R3_001.fastq.gz | R3 |
| 1294_S1_L008_R4_001.fastq.gz | R4 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. A good cutoff value for quality scores is Q20. This indicates that there's a 99% likelihood of a correct base calling. According to the averaged distribution graphs, most sequences should be above that value.
    3.  zcat 1294_S1_L008_R3_001.fastq.gz | sed -n '2~4p' | grep "N" | wc -l = 3328051
        zcat 1294_S1_L008_R2_001.fastq.gz | sed -n '2~4p' | grep "N" | wc -l = 3976613
        Total = 7,304,664

Read1
![](https://github.com/2020-bgmp/demultiplexing-m-chang3/blob/master/Read1QualScoreDist.png)

Read2
![](https://github.com/2020-bgmp/demultiplexing-m-chang3/blob/master/Read2QualScoreDist.png)

Read3
![](https://github.com/2020-bgmp/demultiplexing-m-chang3/blob/master/Read3QualScoreDist.png)

Read4
![](https://github.com/2020-bgmp/demultiplexing-m-chang3/blob/master/Read4QualScoreDist.png)
    
## Part 2
1. Define the problem
2. Describe output
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [4 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
    
    
    
PART 2 PSEUDOCODE:

def rev_comp(sequence):
    '''Calculate the reverse complement of a sequence'''
    Loop through sequence. Create a list to hold complement sequence. Create a list to hold the reverse complement sequence.
    If letter in sequence is A, add T to list. If T, add A. If C, add G. If G, add C.
    Reverse the sequence with index slicing: reverselist[::-1] = revcomp
    Return revcomp

def add_indices(read1[0], read2[1], read3[1], read4[0]):
    '''Update header information for biological sequences to hold index information from BOTH indices'''
    Update header information:
        read1[0] is the header line. Set it equal to the concatenation of read1[0] and read2[1] and read3[1].
        read4[0] is the header line. Set it equal to the concatenation of read4[0] and read2[1] and read3[1].

def categorize_reads(read1, read2, read3, read4):
    '''Split reads into categories based on if indices match or don't match or are unknown'''
    Create a line counter to loop through each file.
    Create four separate 1D numpy arrays of length 4 containing strings.
    Take the first 4 lines from each file to get a single full record.
        Open each file. Write 4 lines at a time to a separate numpy 1D array of length 4 for each file.
    For each record in each numpy array:
        Compare sequences from each record (line 2 in each record).
            Reference sequences by index and array (i.e. read1[1])
        Call function rev_comp(read3). Update array for read 3 sequence to the reverse complement.
        Remove all sequences with any quality scores < 20 for indices only:
            If ANY N's OR any quality scores lower than 20 in read 2 or read 3
                Add read 2 and read 3 sequences to read 1 and read 4 headers with add_indices() function.
                Update header information for reads 1 and 4 numpy arrays to new headers.
                Write updated records for reads 1 and 4 to two separate files called UnknownForward and UnknownReverse (with index info in header)
        Compare index sequences that are known:
            If read 2 and read 3 sequences match:
                Make a dictionary to hold indices as keys and ints as values (starting at 0)
                Add read2 and read 3 sequences to read 1 and read 4 headers with add_indices() function.
                Update header information for reads 1 and 4 numpy arrays to new headers.
                If index in dictionary, add 1 to value
                If index not in dictionary, add to dictionary as key, value = 1
                Write updated records for reads 1 and 4 to two of 48 separate files; Write to a file name called (R1 or R4, index)
            If read 2 and 3 don't match AND don't have any N's in the sequence:
                Make a dictionary to hold indices as keys and ints as values. Permutations will be recorded (not combinations)
                Add read 2 and read 3 sequences to read 1 and read 4 headers with add_indices() function.
                Update header information for reads 1 and 4 numpy arrays to new headers.
                If index not in dictionary (in R2-R3 order), add index to dictionary, value = 1
                If index in dictionary, add 1 to value.
                Write updated records for reads 1 and 4 to two separate files called UnmatchedForward and UnmatchedReverse (with index info in header)
            
        Clear numpy arrays holding record from each file.
        Return 52 files
        
    
