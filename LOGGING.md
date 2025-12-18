# Snakemake Logging Guide

This workflow includes logging at multiple levels to help track execution and debug issues on Great Lakes.

## Log Files Location

All per-rule logs are saved in the `logs/` directory:

```text
logs/
  preprocess_data.log
  clean_data.log
  run_analysis.log
  summarize_results.log
  visualize_results.log
```

## 1. Per-Rule Logging (Easiest)

Each Snakemake rule includes a `log:` directive that captures stdout/stderr:

```python
rule run_analysis:
    input:
        "data/cleaned_data.csv"
    output:
        "results/analysis_output.txt"
    threads: 2
    log:
        "logs/run_analysis.log"
    shell:
        "python -m scripts.helpers run-analysis --input {input} --output {output} > {log} 2>&1"
```

The `> {log} 2>&1` redirects both stdout and stderr to the log file.

## 2. Python Script Logging

In `scripts/helpers.py`, logging is configured at the module level:

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
```

Each function then emits messages:

```python
def run_analysis(input_path: str, output_path: str) -> None:
    logging.info(f"Starting analysis of {input_path}")
    # ... process ...
    logging.info(f"Loaded {len(cases)} cases")
    # ... compute ...
    logging.info(f"Analysis results: {hospitalized} hospitalized, {deaths} deaths")
```

These messages appear in the Snakemake log files.

## 3. Viewing Logs

### Local execution for testing

```bash
# View a specific rule's log
cat logs/run_analysis.log

# Tail all logs in real time
tail -f logs/*.log

# Search logs for errors
grep -i error logs/*.log
```

### On Great Lakes with SLURM

```bash
# View per-rule logs as above
cat logs/run_analysis.log

# View SLURM job logs (if configured)
# Set slurm-logdir in workflow/profiles/slurm/config.yaml
cat logs/slurm/{RULE}/{JOBID}.log

# Check job status in SLURM
squeue -u $USER
sacct -u $USER -o JobID,State,Comment
```

## 4. Configuration

Logging behavior can be controlled via `config/config.yaml`:

```yaml
logging:
  level: "INFO"
  format: "%(asctime)s - %(levelname)s - %(message)s"
```

### SLURM Logging

From the [SLURM executor documentation](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html#log-files-getting-information-on-failures) on SLURM log files:

> By default, the SLURM executor deletes log files of successful jobs immediately after completion (remember: this is redundant information). To modify this behavior and retain logs of successful jobs, use the --slurm-keep-successful-logs flag. Additionally, log files for failed jobs are preserved for 10 days by default. To change this retention period, use the --slurm-delete-logfiles-older-than flag.

## 5. Troubleshooting

If logs are empty:

- Ensure the helper script imports `logging` and calls `logging.info(...)`.
- Check that your shell command has `> {log} 2>&1` to redirect output.
- Run locally first: `snakemake --cores 1` to verify.

If you need more detail:

- Add `--verbose` to the Snakemake command: `snakemake --cores 1 --verbose`
- Increase log level in the helper script: `logging.basicConfig(level=logging.DEBUG, ...)`

## Example Log Output

```text
2025-12-09 13:26:46,470 - INFO - Starting analysis of data/cleaned_data.csv
2025-12-09 13:26:46,470 - INFO - Loaded 20 cases
2025-12-09 13:26:46,470 - INFO - Analysis results: 5 hospitalized, 2 deaths
2025-12-09 13:26:46,470 - INFO - Analysis output written to results/analysis_output.txt
```
