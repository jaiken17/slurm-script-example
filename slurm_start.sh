#!/bin/bash
#SBATCH --time=00:05:00
##SBATCH --account=#{groupName}
#SBATCH --job-name=example_job
#SBATCH --output=output-%x_%j.out
#SBATCH --error=error-%x_%j.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --array=1-3
##SBATCH --mail-user=<#{email}>
##SBATCH --mail-type=END
##SBATCH --mail-type=FAIL

# two '#' means SLURM skips command

# Set location of template working directory and parameters file
TEMPLATE_DIR=template_wd/
PARAMS_FILE=params.txt

# Call python script that copies template dir into a new run dir and sets initial parameters
# Python scripts prints the name of new dir to stdout which is saved to $DIR var here
DIR=$(python3 make_wds.py $PARAMS_FILE $TEMPLATE_DIR $SLURM_ARRAY_TASK_ID)

cd $DIR

# Copy the script that runs the program, and run script with srun (SLURM)
cp ../prog_run.sh .
srun prog_run.sh