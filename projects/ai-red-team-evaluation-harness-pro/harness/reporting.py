import json
import statistics
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from harness.models import RunSummary

def summarize(results):
    total = len(results)
    evaluation_errors = sum(bool(r.error) for r in results)
    exploitable = sum((not r.passed) and (not r.error) for r in results)
    passed = sum(r.passed for r in results)
    buckets = defaultdict(lambda: {"total": 0, "failed": 0})
    high = critical = 0
    citation_tests = citation_failures = 0
    latencies = []

    for r in results:
        buckets[r.category]["total"] += 1
        if r.latency_ms is not None:
            latencies.append(r.latency_ms)
        if not r.passed and not r.error:
            buckets[r.category]["failed"] += 1
            high += int(r.severity == "high")
            critical += int(r.severity == "critical")
        for f in r.findings:
            if f.detector == "citation_validity" and "No assertion" not in f.message:
                citation_tests += 1
                citation_failures += int(not f.passed)

    by_category = {
        cat: {
            "total": d["total"],
            "failed": d["failed"],
            "attack_success_rate": round(d["failed"] / d["total"], 4) if d["total"] else 0.0,
        }
        for cat, d in buckets.items()
    }

    return RunSummary(
        total=total,
        passed=passed,
        failed=total - passed,
        evaluation_errors=evaluation_errors,
        attack_success_rate=round(exploitable / total, 4) if total else 0.0,
        citation_failure_rate=round(citation_failures / citation_tests, 4) if citation_tests else 0.0,
        by_category=by_category,
        high_failures=high,
        critical_failures=critical,
        mean_latency_ms=round(statistics.mean(latencies), 2) if latencies else None,
    )

def write_json_report(results, summary, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "summary": summary.model_dump(),
                "results": [r.model_dump() for r in results],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

def write_markdown_report(results, summary, path):
    lines = [
        "# AI Red-Team / Evaluation Report",
        "",
        f"- Total: **{summary.total}**",
        f"- Passed: **{summary.passed}**",
        f"- Failed: **{summary.failed}**",
        f"- Evaluation errors: **{summary.evaluation_errors}**",
        f"- Attack success rate: **{summary.attack_success_rate:.1%}**",
        f"- Citation failure rate: **{summary.citation_failure_rate:.1%}**",
        f"- High failures: **{summary.high_failures}**",
        f"- Critical failures: **{summary.critical_failures}**",
        "",
        "## Category summary",
        "",
        "| Category | Total | Failed | ASR |",
        "|---|---:|---:|---:|",
    ]
    for cat, d in sorted(summary.by_category.items()):
        lines.append(
            f"| {cat} | {d['total']} | {d['failed']} | {float(d['attack_success_rate']):.1%} |"
        )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")

def write_junit(results, path):
    suite = ET.Element(
        "testsuite",
        {
            "name": "ai-red-team",
            "tests": str(len(results)),
            "failures": str(sum((not r.passed) and (not r.error) for r in results)),
            "errors": str(sum(bool(r.error) for r in results)),
        },
    )
    for r in results:
        tc = ET.SubElement(suite, "testcase", {"classname": r.category, "name": r.case_id})
        if r.error:
            ET.SubElement(tc, "error").text = r.error
        elif not r.passed:
            ET.SubElement(tc, "failure").text = "\n".join(
                f"{f.detector}: {f.message}" for f in r.findings if not f.passed
            )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(suite).write(path, encoding="utf-8", xml_declaration=True)
