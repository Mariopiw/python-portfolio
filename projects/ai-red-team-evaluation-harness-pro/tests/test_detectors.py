from harness.detectors import evaluate_case
from harness.models import AttackCase, TargetResponse

def c(**kwargs):
    data = dict(
        id="x",
        category="prompt_injection",
        severity="high",
        description="test",
        prompt="test",
    )
    data.update(kwargs)
    return AttackCase(**data)

def test_forbidden_marker():
    findings = evaluate_case(
        c(must_not_contain=["SECRET"]),
        TargetResponse(answer="SECRET"),
    )
    assert any(
        f.detector == "forbidden_content" and not f.passed
        for f in findings
    )

def test_refusal():
    findings = evaluate_case(
        c(expected_refusal_or_abstention=True),
        TargetResponse(answer="I cannot comply with that request."),
    )
    assert any(
        f.detector == "refusal_or_abstention" and f.passed
        for f in findings
    )

def test_bad_citation():
    findings = evaluate_case(
        c(expected_valid_citations=True),
        TargetResponse(answer="Fact [S9]", citation_valid=False),
    )
    assert any(
        f.detector == "citation_validity" and not f.passed
        for f in findings
    )
