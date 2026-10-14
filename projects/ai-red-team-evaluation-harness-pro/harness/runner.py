from rich.console import Console
from harness.detectors import evaluate_case
from harness.models import CaseResult
from harness.targets.factory import build_target

console = Console()

class HarnessRunner:
    def __init__(self, config: dict):
        self.config = config
        self.target = build_target(config)
        self.stop_on_critical = bool(config["run"].get("stop_on_critical", False))

    def run_case(self, case):
        try:
            self.target.prepare_case(case)
            response = self.target.execute(case)
            findings = evaluate_case(case, response)
            passed = all(f.passed for f in findings)
            return CaseResult(
                case_id=case.id, category=case.category, severity=case.severity,
                passed=passed, attack_succeeded=not passed,
                answer=response.answer, sources=response.sources,
                findings=findings, latency_ms=response.raw.get("_latency_ms")
            )
        except Exception as exc:
            return CaseResult(
                case_id=case.id, category=case.category, severity=case.severity,
                passed=False, attack_succeeded=False, answer="", error=str(exc)
            )

    def run(self, cases):
        results = []
        for i, case in enumerate(cases, 1):
            console.print(f"[bold]{i}/{len(cases)}[/bold] {case.category} :: {case.id}")
            result = self.run_case(case)
            results.append(result)
            console.print(
                "  [yellow]ERROR[/yellow]" if result.error
                else ("  [green]PASS[/green]" if result.passed else "  [red]FAIL[/red]")
            )
            if self.stop_on_critical and not result.passed and not result.error and result.severity == "critical":
                break
        return results
