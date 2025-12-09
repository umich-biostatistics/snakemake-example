"""
Analysis and visualization rules: compute statistics and generate outputs.
"""

rule run_analysis:
    input:
        "data/cleaned_data.csv"
    output:
        "results/analysis_output.txt"
    resources:
        mem_mb=1024,
        runtime=15,
        cpus_per_task=2
    threads: 2
    log:
        "logs/run_analysis.log"
    message:
        "Running statistical analysis on cleaned data (using {threads} threads)"
    shell:
        "python -m scripts.helpers run-analysis --input {input} --output {output} > {log} 2>&1" 


rule summarize_results:
    input:
        "results/analysis_output.txt"
    output:
        "results/summary.txt"
    resources:
        mem_mb=512,
        runtime=5,
        cpus_per_task=1
    threads: 1
    log:
        "logs/summarize_results.log"
    message:
        "Summarizing analysis results"
    shell:
        "python -m scripts.helpers summarize --input {input} --output {output} > {log} 2>&1" 


rule visualize_results:
    input:
        "results/summary.txt"
    output:
        "results/visualization.png"
    resources:
        mem_mb=512,
        runtime=10,
        cpus_per_task=1
    threads: 1
    log:
        "logs/visualize_results.log"
    message:
        "Generating visualization from summary"
    shell:
        "python -m scripts.helpers visualize --input {input} --output {output} > {log} 2>&1" 