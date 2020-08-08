#!/bin/bash
#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --account=bgmp          ### Account used for job submission
#SBATCH --nodes=1
#SBATCH --time=3-00:00:00
#SBATCH --error=%j_demultiplex.err
#SBATCH --output=%j_demultiplex.out
#SBATCH --ntasks-per-node=1
#SBATCH --mail-user=mchang3@uoregon.edu
#SBATCH --mail-type=ALL


conda activate bgmp_py37
/usr/bin/time -v \
./demultiplex5withavgqscores.py -f1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -f2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-f3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -f4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -f5 /projects/bgmp/shared/2017_sequencing/indexes.txt \

