# Snakemake Workflow Example

This project demonstrates a modular, reproducible data analysis workflow using Snakemake. It is designed to run efficiently on both local machines and high-performance computing clusters (e.g., Great Lakes at the University of Michigan) via SLURM job submission.

**Key Features:**

- Single workflow runs on local and cluster systems
- Explicit resource declarations per rule
- Informative progress messages and logging
- Flexible profile system for different execution environments

## Project Structure

- **config/**: Contains workflow-level configuration consumed by the Snakefile and rules.
  - `config.yaml`: Defines workflow paths (data, results, logs) plus workflow parameters such as the preprocessing delimiter and final target.

- **envs/**: Contains conda environment specifications.
  - `smk-ex.yaml`: Defines the base conda environment for the example, requirements and dependencies not actually used.

- **logs/**: Directory for storing log files generated during the execution of the Snakemake workflow.

- **rules/**: Contains rule files that define the workflow's execution order and dependencies.
  - `all.smk`: Main rule file that specifies the final output of the workflow.
  - `analysis.smk`: Rules specific to the analysis steps of the workflow.
  - `preprocess.smk`: Rules for preprocessing the data before analysis.

- **Snakefile**: The main file that orchestrates the Snakemake workflow, importing rules from the `rules` directory and defining the overall workflow structure. Includes documentation and usage examples.

- **workflow/**: Contains profiles and configurations for the workflow.
  - **profiles/slurm/**: SLURM profile that enables cluster job submission.
    - `config.yaml`: Defines the executor (`slurm`), sets default resources (partition, account, runtime, memory, CPUs), and parallel job limits.

## Setup Instructions

1. **Environment Setup**: Create the conda environments specified in the `envs` directory using the provided YAML files.

    ```bash
    conda env create -f envs/smk-ex.yaml
    ```

1. **Configuration**:

    - Workflow paths and rule parameters: edit `config/config.yaml`.
    - Cluster resources (partition, account, memory, CPUs, runtime): edit `workflow/profiles/slurm/config.yaml` under `default-resources`.

1. **Running the Workflow**:

   **Local execution (recommended for testing):**
   ```bash
   snakemake --cores 4
   ```

   **SLURM cluster execution (after configuring account and partition):**
   ```bash
   snakemake --profile workflow/profiles/slurm
   ```
   
   **Dry run (preview without executing):**
   ```bash
   snakemake --cores 4 --dry-run
   ```

## Resource Requirements

The workflow defines realistic resource requirements per rule:

| Rule | Memory | Runtime | Cores |
|------|--------|---------|-------|
| preprocess_data | 512 MB | 5 min | 1 |
| clean_data | 512 MB | 5 min | 1 |
| run_analysis | 1024 MB | 15 min | 2 |
| summarize_results | 512 MB | 5 min | 1 |
| visualize_results | 512 MB | 10 min | 1 |
| **Total** | - | **40 min** | - |

## Usage Guidelines

- **Logs**: Monitor progress and errors in the `logs/` directory. Each rule generates its own log file.
- **Modifications**: Edit rules in the `rules/` directory to customize the analysis pipeline.
- **Parameters**: Update workflow parameters in `config/config.yaml` (delimiter, paths, etc.).
- **SLURM Users**: Before first cluster execution, configure `workflow/profiles/slurm/config.yaml`:
  - Set `slurm_account` to your SLURM account (check with `sacctmgr list accounts`)
  - Set `slurm_partition` to your default partition (check with `sinfo`)
- **Progress Tracking**: Each rule includes a `message:` directive that prints when executed, helping you track workflow progress.

## Troubleshooting

**Workflow doesn't run:**
- Check that data files exist in `data/`
- Verify Python scripts in `scripts/` are executable
- Run `snakemake --cores 4 --dry-run` to identify issues

**SLURM job fails:**
- Check job logs in `logs/slurm_logs/` for error details
- Verify account and partition names match your SLURM configuration
- Increase resource limits in `workflow/profiles/slurm/config.yaml` if jobs timeout
