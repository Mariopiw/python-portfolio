import argparse
import sys

from rich.console import Console
from rich.table import Table

from harness.dataset import load_cases
from harness.gates import evaluate_gates
from harness.regression import compare, save_baseline
from harness.reporting import summarize, write_json_report, write_junit, write_markdown_report
from harness.runner import HarnessRunner
from harness.settings import load_config

console = Console()

def main():
    parser = argparse.ArgumentParser(description="AI Red-Team / Evaluation Harness Pro")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--dataset-dir", default="datasets")
    parser.add_argument("--update-baseline", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    cases = load_cases(args.dataset_dir, config["run"]["categories"])

    if not cases:
        console.print("[red]No test cases loaded.[/red]")
        return 2

    results = HarnessRunner(config).run(cases)
    summary = summarize(results)

    reporting = config["reporting"]
    write_json_report(results, summary, reporting["json"])
    write_markdown_report(results, summary, reporting["markdown"])
    write_junit(results, reporting["junit"])

    table = Table(title="AI Red-Team Summary")
    table.add_column("Category")
    table.add_column("Total", justify="right")
    table.add_column("Failed", justify="right")
    table.add_column("ASR", justify="right")

    for category, data in sorted(summary.by_category.items()):
        table.add_row(
            category,
            str(data["total"]),
            str(data["failed"]),
            f"{float(data['attack_success_rate']):.1%}",
        )

    console.print(table)
    console.print(f"Overall ASR: [bold]{summary.attack_success_rate:.1%}[/bold]")
    console.print(f"Citation failure rate: {summary.citation_failure_rate:.1%}")

    gates_ok, gate_problems = evaluate_gates(summary, config)
    for item in gate_problems:
        console.print(f"[red]Gate:[/red] {item}")

    regression = config["regression"]
    regression_ok, regression_problems = compare(
        summary,
        regression["baseline_file"],
        float(regression["max_overall_asr_increase"]),
        float(regression["max_category_asr_increase"]),
        float(regression["max_citation_failure_rate_increase"]),
    )
    for item in regression_problems:
        console.print(f"[yellow]Regression:[/yellow] {item}")

    if args.update_baseline:
        save_baseline(summary, regression["baseline_file"])
        console.print(f"[green]Baseline saved:[/green] {regression['baseline_file']}")

    return 0 if gates_ok and regression_ok else 1

if __name__ == "__main__":
    sys.exit(main())
