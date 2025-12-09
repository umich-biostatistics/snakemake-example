# Great Lakes Snakemake Workflow

This project is designed to facilitate data analysis using Snakemake on the Great Lakes cluster at the University of Michigan. Below is an overview of the project's structure and components.

## Project Structure

- **config/**: Contains workflow-level configuration consumed by the Snakefile and rules.
  - `config.yaml`: Defines workflow paths (data, results, logs) plus workflow parameters such as the preprocessing delimiter and final target.

- **envs/**: Contains conda environment specifications.
  - `analysis.yaml`: Specifies the conda environment for the analysis, including the required packages and their versions.
  - `base.yaml`: Defines the base conda environment, which may include common dependencies needed across different workflows.

- **logs/**: Directory for storing log files generated during the execution of the Snakemake workflow.

- **rules/**: Contains rule files that define the workflow's execution order and dependencies.
  - `all.smk`: Main rule file that specifies the final output of the workflow.
  - `analysis.smk`: Rules specific to the analysis steps of the workflow.
  - `preprocess.smk`: Rules for preprocessing the data before analysis.

- **Snakefile**: The main file that orchestrates the Snakemake workflow, importing rules from the `rules` directory and defining the overall workflow structure.

- **workflow/**: Contains profiles and configurations for the workflow.
  - **profiles/slurm/**: SLURM profile that enables the `snakemake-executor-plugin-slurm` plugin.
    - `config.yaml`: Defines the executor (`slurm`), points to `config/config.yaml`, and sets default resources (partition, account, runtime, memory, CPUs).

## Setup Instructions

1. **Environment Setup**: Create the conda environments specified in the `envs` directory using the provided YAML files.

    ```bash
    conda env create -f envs/base.yaml
    conda env create -f envs/analysis.yaml
    ```

1. **Configuration**:

    - Workflow paths and rule parameters: edit `config/config.yaml`.
    - Cluster resources (partition, account, memory, CPUs, runtime): edit `workflow/profiles/slurm/config.yaml` under `default-resources`.

1. **Running the Workflow**: Execute Snakemake with the Great Lakes profile (adjust `--jobs` as needed):

    ```bash
    snakemake --profile workflow/profiles/slurm --jobs 150
    ```

## Usage Guidelines

- Ensure that you have access to the Great Lakes cluster and the necessary permissions to submit jobs using SLURM.
- Monitor the logs in the `logs/` directory for any issues or progress updates during the workflow execution.
- Modify the rules in the `rules` directory as needed to accommodate your specific analysis requirements.

## Workflow Components

Each component of the workflow is designed to be modular, allowing for easy updates and modifications. The use of Snakemake ensures reproducibility and efficient resource management during the analysis process.
