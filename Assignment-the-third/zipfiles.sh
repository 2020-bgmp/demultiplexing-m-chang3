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


gzip *___* \
gzip Un*
