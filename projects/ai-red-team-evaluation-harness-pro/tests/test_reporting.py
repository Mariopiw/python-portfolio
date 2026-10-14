from harness.models import CaseResult
from harness.reporting import summarize

def test_summary():
    results = [
        CaseResult(
            case_id="a",
            category="prompt_injection",
            severity="high",
            passed=True,
            attack_succeeded=False,
            answer="safe",
        ),
        CaseResult(
            case_id="b",
            category="prompt_injection",
            severity="critical",
            passed=False,
            attack_succeeded=True,
            answer="unsafe",
        ),
    ]

    summary = summarize(results)

    assert summary.total == 2
    assert summary.attack_success_rate == 0.5
    assert summary.critical_failures == 1
