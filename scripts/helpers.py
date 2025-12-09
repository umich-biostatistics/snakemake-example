import argparse
import csv
import os
import sys
import logging
from collections import Counter

# Setup logging to capture in Snakemake logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)


def preprocess(input_path: str, output_path: str, delimiter: str = ",") -> None:
    """Preprocess CSV: remove blank rows, keep header and valid data rows."""
    logging.info(f"Starting preprocessing of {input_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, newline="") as in_f, open(output_path, "w", newline="") as out_f:
        reader = csv.reader(in_f, delimiter=delimiter)
        writer = csv.writer(out_f, delimiter=delimiter)
        rows_read = 0
        rows_written = 0
        for row in reader:
            rows_read += 1
            # Keep header and non-empty rows
            if any(cell.strip() for cell in row):
                writer.writerow(row)
                rows_written += 1
    logging.info(f"Preprocessing complete: {rows_read} rows read, {rows_written} rows written to {output_path}")


def clean(input_path: str, output_path: str) -> None:
    """Clean CSV: remove duplicate rows while preserving order and header."""
    logging.info(f"Starting cleaning of {input_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    seen = set()
    rows_read = 0
    rows_written = 0
    with open(input_path) as in_f, open(output_path, "w") as out_f:
        for line in in_f:
            rows_read += 1
            if line not in seen:
                seen.add(line)
                out_f.write(line)
                rows_written += 1
    logging.info(f"Cleaning complete: {rows_read} rows read, {rows_written} unique rows written to {output_path}")


def run_analysis(input_path: str, output_path: str) -> None:
    """Analyze surveillance data: compute case counts, outcomes, vaccination status."""
    logging.info(f"Starting analysis of {input_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cases = []
    with open(input_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(row)
    
    logging.info(f"Loaded {len(cases)} cases")
    total_cases = len(cases)
    disease_counts = Counter(c.get("disease", "") for c in cases)
    outcome_counts = Counter(c.get("outcome", "") for c in cases)
    vax_counts = Counter(c.get("vaccination_status", "") for c in cases)
    
    hospitalized = sum(1 for c in cases if c.get("outcome") == "Hospitalized")
    deaths = sum(1 for c in cases if c.get("outcome") == "Death")
    
    logging.info(f"Analysis results: {hospitalized} hospitalized, {deaths} deaths")
    
    with open(output_path, "w") as out_f:
        out_f.write(f"total_cases\t{total_cases}\n")
        out_f.write(f"hospitalized\t{hospitalized}\n")
        out_f.write(f"deaths\t{deaths}\n")
        out_f.write("\nby_disease\n")
        for disease, count in disease_counts.most_common():
            out_f.write(f"  {disease}\t{count}\n")
        out_f.write("\nby_outcome\n")
        for outcome, count in outcome_counts.most_common():
            out_f.write(f"  {outcome}\t{count}\n")
        out_f.write("\nby_vaccination\n")
        for vax, count in vax_counts.most_common():
            out_f.write(f"  {vax}\t{count}\n")
    
    logging.info(f"Analysis output written to {output_path}")


def summarize(input_path: str, output_path: str) -> None:
    """Summarize epidemiological metrics: rates, proportions, CFR."""
    logging.info(f"Starting summarization of {input_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    stats = {}
    with open(input_path) as in_f:
        for line in in_f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                key, val_str = parts[0], parts[1]
                if key in ["total_cases", "hospitalized", "deaths"]:
                    try:
                        stats[key] = int(val_str)
                    except ValueError:
                        pass
    
    total = stats.get("total_cases", 1)
    hosp = stats.get("hospitalized", 0)
    deaths = stats.get("deaths", 0)
    
    hosp_rate = (hosp / total * 100) if total > 0 else 0
    cfr = (deaths / total * 100) if total > 0 else 0
    
    logging.info(f"Computed rates: Hospitalization={hosp_rate:.1f}%, CFR={cfr:.1f}%")
    
    with open(output_path, "w") as out_f:
        out_f.write(f"metric\tvalue\n")
        out_f.write(f"Total Cases\t{total}\n")
        out_f.write(f"Hospitalized\t{hosp}\n")
        out_f.write(f"Deaths\t{deaths}\n")
        out_f.write(f"Hospitalization Rate (%)\t{hosp_rate:.1f}\n")
        out_f.write(f"Case Fatality Rate (%)\t{cfr:.1f}\n")
    
    logging.info(f"Summary written to {output_path}")


def visualize(input_path: str, output_path: str) -> None:
    """Create epidemiological summary dashboard: outcomes and rates."""
    logging.info(f"Starting visualization of {input_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    import matplotlib.pyplot as plt

    metrics = {}
    with open(input_path) as in_f:
        reader = csv.DictReader(in_f, delimiter="\t")
        for row in reader:
            if row.get("metric") and row.get("value"):
                try:
                    metrics[row["metric"]] = float(row["value"])
                except (ValueError, TypeError):
                    pass

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("Disease Surveillance Summary", fontsize=14, fontweight="bold")

    # Case counts
    total = metrics.get("Total Cases", 0)
    hosp = metrics.get("Hospitalized", 0)
    deaths = metrics.get("Deaths", 0)
    recovered = total - hosp - deaths
    
    outcomes = ["Recovered", "Hospitalized", "Deaths"]
    counts = [recovered, hosp, deaths]
    colors = ["#2ecc71", "#f39c12", "#e74c3c"]
    ax1.bar(outcomes, counts, color=colors)
    ax1.set_ylabel("Count")
    ax1.set_title("Outcomes by Case Status")
    ax1.tick_params(axis="x", rotation=45)

    # Rates
    hosp_rate = metrics.get("Hospitalization Rate (%)", 0)
    cfr = metrics.get("Case Fatality Rate (%)", 0)
    rate_labels = ["Hospitalization\nRate", "Case Fatality\nRate"]
    rate_values = [hosp_rate, cfr]
    ax2.bar(rate_labels, rate_values, color=["#3498db", "#e74c3c"])
    ax2.set_ylabel("Percentage (%)")
    ax2.set_title("Key Epidemiological Rates")
    ax2.set_ylim(0, max(rate_values) * 1.2 if rate_values else 100)
    
    # Case summary text
    ax3.text(0.5, 0.7, f"Total Cases: {int(total)}", ha="center", fontsize=12, weight="bold")
    ax3.text(0.5, 0.5, f"Hospitalized: {int(hosp)}", ha="center", fontsize=11)
    ax3.text(0.5, 0.3, f"Deaths: {int(deaths)}", ha="center", fontsize=11)
    ax3.axis("off")
    ax3.set_title("Case Summary")

    # Rate summary text
    ax4.text(0.5, 0.7, f"Hospitalization Rate: {hosp_rate:.1f}%", ha="center", fontsize=11)
    ax4.text(0.5, 0.5, f"CFR: {cfr:.1f}%", ha="center", fontsize=11)
    ax4.text(0.5, 0.3, "(Case Fatality Rate)", ha="center", fontsize=9, style="italic")
    ax4.axis("off")
    ax4.set_title("Epidemic Metrics")

    plt.tight_layout()
    fig.savefig(output_path, dpi=100)
    plt.close(fig)
    
    logging.info(f"Visualization saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Helper CLI for demo Snakemake workflow")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_pre = subparsers.add_parser("preprocess", help="Preprocess CSV data")
    p_pre.add_argument("--input", required=True)
    p_pre.add_argument("--output", required=True)
    p_pre.add_argument("--delimiter", default=",")

    p_clean = subparsers.add_parser("clean", help="Clean processed data")
    p_clean.add_argument("--input", required=True)
    p_clean.add_argument("--output", required=True)

    p_run = subparsers.add_parser("run-analysis", help="Run text analysis")
    p_run.add_argument("--input", required=True)
    p_run.add_argument("--output", required=True)

    p_sum = subparsers.add_parser("summarize", help="Summarize analysis output")
    p_sum.add_argument("--input", required=True)
    p_sum.add_argument("--output", required=True)

    p_viz = subparsers.add_parser("visualize", help="Visualize summary as PNG")
    p_viz.add_argument("--input", required=True)
    p_viz.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "preprocess":
        preprocess(args.input, args.output, args.delimiter)
    elif args.command == "clean":
        clean(args.input, args.output)
    elif args.command == "run-analysis":
        run_analysis(args.input, args.output)
    elif args.command == "summarize":
        summarize(args.input, args.output)
    elif args.command == "visualize":
        visualize(args.input, args.output)


if __name__ == "__main__":
    main()
