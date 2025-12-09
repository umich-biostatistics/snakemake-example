rule preprocess_data:
    input:
        "data/raw_data.csv"
    output:
        "data/processed_data.csv"
    params:
        delimiter = config["workflow"]["preprocess_delimiter"]
    log:
        "logs/preprocess_data.log"
    shell:
        "python -m scripts.helpers preprocess --input {input} --output {output} --delimiter {params.delimiter} > {log} 2>&1"

rule clean_data:
    input:
        "data/processed_data.csv"
    output:
        "data/cleaned_data.csv"
    log:
        "logs/clean_data.log"
    shell:
        "python -m scripts.helpers clean --input {input} --output {output} > {log} 2>&1"