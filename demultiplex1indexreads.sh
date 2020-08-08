#!/bin/bash
#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=R2R3   ### Job Name
#SBATCH --time=0-06:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=1     ### Number of tasks to be launched per Node
#SBATCH --cpus-per-task=1       ### Number of tasks to be launched
#SBATCH --account=bgmp          ### Account used for job submission

conda activate bgmp_py37

/usr/bin/time -v ./demultiplex1index.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -gn Read2

/usr/bin/time -v ./demultiplex1index.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -gn Read3
