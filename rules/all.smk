"""
Final workflow rule: defines the expected outputs of the entire pipeline.
"""

rule all:
    input:
        expand(config["workflow"]["final_output"])
    message:
        "All workflow steps completed successfully!"