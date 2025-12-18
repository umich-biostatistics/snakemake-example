#!/bin/bash

#SBATCH --job-name=snakemake-controller
#SBATCH --partition=standard
#SBATCH --account=yourAccount0
#SBATCH --time=10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1GB
#SBATCH --output=logs/controller.log

# Load the conda/mamba module
module load mamba

# Run Snakemake from the snakemake environment with recovery-oriented flags
# --rerun-incomplete: re-run jobs that produced incomplete output after a crash
# --restart-times 3: retry failed jobs up to 3 times for transient failures
# --latency-wait 60: wait up to 60s for expected output files to appear on shared filesystems
conda run --live-stream -n snakemake snakemake \
    --workflow-profile workflow/profiles/slurm \
    --default-resources slurm_account="yourAccount0" slurm_partition="standard" \
    --sdm conda \
    --rerun-incomplete --restart-times 3 --latency-wait 60 "$@"
