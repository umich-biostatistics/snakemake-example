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

rule summarize_results:
    input:
        "results/analysis_output.txt"
    output:
        "results/summary.txt"
    threads: 1
    log:
        "logs/summarize_results.log"
    shell:
        "python -m scripts.helpers summarize --input {input} --output {output} > {log} 2>&1" 

rule visualize_results:
    input:
        "results/summary.txt"
    output:
        "results/visualization.png"
    threads: 1
    log:
        "logs/visualize_results.log"
    shell:
        "python -m scripts.helpers visualize --input {input} --output {output} > {log} 2>&1" 