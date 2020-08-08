#!/usr/bin/env python
import argparse
import itertools
import re
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="Specify input filenames")
    parser.add_argument("-f1", "--filenameforRead1", help="FilenameR1", required=True)
    parser.add_argument("-f2", "--filenameforRead2", help="FileNameR2", required=True)
    parser.add_argument("-f3", "--filenameforRead3", help="FilenameR3", required=True)
    parser.add_argument("-f4", "--filenameforRead4", help="FilenameR4", required=True)
    parser.add_argument("-f5", "--filenameforIndices", help="Indices", required=True)
    return parser.parse_args()
args = get_args()
f1 = args.filenameforRead1
f2 = args.filenameforRead2
f3 = args.filenameforRead3
f4 = args.filenameforRead4
f5 = args.filenameforIndices

#Create a Reverse Complement Function
def revcomp(sequence):
    '''This code is to create a reverse complement of a given sequence'''
    complement = []
    for i in sequence:
        if i == "A":
            complement.append("T")
        elif i == "T":
            complement.append("A")
        elif i == "G":
            complement.append("C")
        elif i == "C":
            complement.append("G")
        else:
            complement.append("N")

    revcomp = str(complement[::-1]).replace("[", "").replace("]", "").replace(" ", "").replace(",","").replace("'", "")
    return revcomp

indexdict = {}

#Create a dictionary with all index information in it.
#Sequences are keys, values are the rest of the information
firstline = True
with open(f5, "r") as f5:

    for line in f5:
        if firstline == True: #Take out the first line in indexes file containing column headers
            firstline = False
            continue
        x = line.split("\t")
        indexdict[x[4].strip()] = str(x[0] + "_" + x[1] + "_" + x[2] + "_" + x[3])



#Create a dictionary with all possible permutations of indices
#Keys are permutation tuples, values are all 0
perm_dict = {}
for i in itertools.product(indexdict.keys(), repeat = 2):
    perm_dict[i] = 0



#Create 48 matched files (forward and reverse for each index)
#index as key, other info added to file name

def convert_phred(x):
    '''Converts a single character into a phred 33 score'''
    phred = (ord(x) - 33)
    return phred

#Put in counter variables for unknown / unmatched
unknowncount = 0
unmatchedcount = 0
###############################################################################################################################################################
#MAIN FUNCTION BELOW
###############################################################################################################################################################


#Open All Input Files and the Output Files for Unknown and Unmatched and Stats
#Open All Input Files and the Output Files for Unknown and Unmatched and Stats
with gzip.open(f1, "rt") as f1, gzip.open(f2, "rt") as f2, gzip.open(f3, "rt") as f3, gzip.open(f4, "rt") as f4:
    with open("UnmatchedForward.fastq", "w") as unmatchedforward, open("UnmatchedReverse.fastq", "w") as unmatchedreverse:
        with open("UnknownForward.fastq", "w") as unknownforward, open("UnknownReverse.fastq", "w") as unknownreverse:

            filehandledict = {}
            #Open all matched Output Files
            for index_seq in indexdict.keys():
                fnwindexinfoRead1 = open("{}___FORWARD_S1_L008_R1_001.fastq".format(indexdict[index_seq]), "w")
                fnwindexinfoRead4 = open("{}___REVERSE_S1_L008_R4_001.fastq".format(indexdict[index_seq]), "w")
                filehandledict[index_seq] = (fnwindexinfoRead1, fnwindexinfoRead4)



            while True: # Input a single record from reads 1 to 4 simultaneously then continue to the next record once done. Records write over themselves once function has been carried out
                header1 = f1.readline().strip()
                if header1 == '':
                    break #EOF break: if header 1 is empty, there are no more records to read in
                seq1 = f1.readline().strip()
                plus1 = f1.readline().strip()
                qscore1 = f1.readline().strip()
                header2 = f2.readline().strip()
                seq2 = f2.readline().strip()
                plus2 = f2.readline().strip()
                qscore2 = f2.readline().strip()
                header3 = f3.readline().strip()
                seq3 = revcomp(f3.readline().strip()) #Revcomp Seq 3 here
                plus3 = f3.readline().strip()
                qscore3 = f3.readline().strip()
                header4 = f4.readline().strip()
                seq4 = f4.readline().strip()
                plus4 = f4.readline().strip()
                qscore4 = f4.readline().strip()
                
                #Append Indexes to header lines
                header1 = str(header1) + "__" + str(seq2) + "__" + str(seq3)
                header4 = str(header4) + "__" + str(seq2) + "__" + str(seq3)
            
              
                
                #Check Quality Scores in Index 1 and Index 2.
                # If qual score < 30 (INCLUDING ANY N'S), output to unknown files 
                sumphredscores = 0
                numberofphreds = 0
                foundbadapple = False
                for i in range(len(qscore2)):
                    
                    sumphredscores += (convert_phred(qscore2[i]) + convert_phred(qscore3[i]))
                    
                    numberofphreds += 2
                averagephredscore = sumphredscores/numberofphreds

                if averagephredscore < 30.0 or "N" in seq2 or "N" in seq3:
                    foundbadapple = True
                    
                    
                
                
                if foundbadapple:
                    
                    #Write Record to Unknown Forward
                    unknownforward.write('{}\n{}\n{}\n{}\n'.format(header1, seq1, plus1, qscore1))
                
                    #Write Record to Unknown Reverse
                    unknownreverse.write('{}\n{}\n{}\n{}\n'.format(header4, seq4, plus4, qscore4))

                    #Increment unknowncount counter
                    unknowncount += 1

                
                #If Index 1 and Index 2 don't match, output to unmatched.
                elif seq2 != seq3:

                    #Update Permutations Dictionary
                    thistup = ()
                    thistup = thistup + (seq2, )
                    thistup = thistup + (seq3, )
                    for i in perm_dict.keys():
                        
                        if i == thistup:
                            
                            perm_dict[i] += 1
                            
                    #Write Read1 Record to Unmatched Forward
                    unmatchedforward.write('{}\n{}\n{}\n{}\n'.format(header1, seq1, plus1, qscore1))
                    
                    #Write Read4 Record to Unmatched Reverse
                    unmatchedreverse.write('{}\n{}\n{}\n{}\n'.format(header4, seq4, plus4, qscore4))
                    
                    #Increment unmatched counter
                    unmatchedcount += 1
                
                #If Index 1 and 2 DO match then output to forward and reverse files named with index information
                elif seq2 == seq3:
                    
                    #Update Permutations Dictionary
                    thistup = ()
                    thistup = thistup + (seq2, )
                    thistup = thistup + (seq3, )
                    for i in perm_dict.keys():
                        
                        if i == thistup:
                            
                            perm_dict[i] += 1

                            
                            (fnwindexinfoRead1, fnwindexinfoRead4) = filehandledict[seq2]

                            #Write Read 1 to file with index name in title
                            fnwindexinfoRead1.write('{}\n{}\n{}\n{}\n'.format(header1, seq1, plus1, qscore1))

                            #Write Read 4 to file with index name in title
                            fnwindexinfoRead4.write('{}\n{}\n{}\n{}\n'.format(header4, seq4, plus4, qscore4))
                    
                    if thistup not in perm_dict.keys(): #Filter out matched pairs of primers not detailed in indexes.txt
                    
                        #Write Record to Unknown Forward
                        unknownforward.write('{}\n{}\n{}\n{}\n'.format(header1, seq1, plus1, qscore1))
                    
                        #Write Record to Unknown Reverse
                        unknownreverse.write('{}\n{}\n{}\n{}\n'.format(header4, seq4, plus4, qscore4))

                        #Increment unknowncount counter
                        unknowncount += 1

#Close all Files

for x,y in filehandledict.values():
    x.close()
    y.close()


#Compile Statistics on the reads:

with open("StatsFile.fastq", "w") as stats:
    #Calculate Total Matched Reads
    totalmatchedreads = 0
    for i in perm_dict.values():
        totalmatchedreads += i
    
    #Calculate Total Reads
    totalreads = totalmatchedreads + unknowncount + unmatchedcount
    stats.write("{}    Total Number of Reads \n".format(totalreads))

    #Calculate overall amount of index hopping
    percentindexhopping = unmatchedcount/totalreads * 100
    stats.write("{}__Total Amount of Index Hopping \n".format(percentindexhopping))

    #Calculate percentage of unknowns
    percentunknown = unknowncount/totalreads*100
    stats.write("{}__Total Amount of Unknown Reads \n".format(percentunknown))

    #Calculate percentage of matched, known reads
    percentmatched = totalmatchedreads/totalreads*100
    stats.write("{}__Total Amount of Matched, Known Reads \n".format(percentmatched))

    #Calculate percentage reads per pair of indices.
    for key in perm_dict:
        percenttotalreads = 100*perm_dict[key]/totalreads
        stats.write("{}__{}percent of total reads \n".format(key, percenttotalreads))
    


