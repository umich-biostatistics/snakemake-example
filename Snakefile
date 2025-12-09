configfile: "config/config.yaml"

rule all:
    input:
        config["workflow"]["final_output"]

include: "rules/preprocess.smk"
include: "rules/analysis.smk"