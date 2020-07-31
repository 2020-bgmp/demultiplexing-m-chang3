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
![](https://github.com/2020-bgmp/demultiplexing-m-chang3/blob/master/*.png)


    
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
