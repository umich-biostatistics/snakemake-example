"""
Data preprocessing rules: input validation, formatting, and cleaning.
"""

rule preprocess_data:
    input:
        "data/raw_data.csv"
    output:
        "data/processed_data.csv"
    conda:
        "envs/smk-ex.yaml"
    params:
        delimiter=config["workflow"]["preprocess_delimiter"]
    resources:
        mem_mb=512,
        runtime=5,
        cpus_per_task=1
    threads: 1
    log:
        "logs/preprocess_data.log"
    message:
        "Preprocessing raw data from {input}"
    shell:
        "python -m scripts.helpers preprocess --input {input} --output {output} --delimiter {params.delimiter} > {log} 2>&1"


rule clean_data:
    input:
        "data/processed_data.csv"
    output:
        "data/cleaned_data.csv"
    conda:
        "envs/smk-ex.yaml"
    resources:
        mem_mb=512,
        runtime=5,
        cpus_per_task=1
    threads: 1
    log:
        "logs/clean_data.log"
    message:
        "Cleaning processed data: removing duplicates"
    shell:
        "python -m scripts.helpers clean --input {input} --output {output} > {log} 2>&1"