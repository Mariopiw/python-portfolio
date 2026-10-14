from typing import Any, Literal
from pydantic import BaseModel, Field

Category = Literal[
    "prompt_injection","rag_poisoning","data_leakage","hallucination",
    "citation_accuracy","tenant_isolation","agent_authorization"
]

class AttackCase(BaseModel):
    id: str
    category: Category
    severity: Literal["low","medium","high","critical"]
    description: str
    prompt: str | None = None
    must_not_contain: list[str] = Field(default_factory=list)
    must_contain_any: list[str] = Field(default_factory=list)
    expected_refusal_or_abstention: bool = False
    expected_valid_citations: bool | None = None
    expected_source_filenames: list[str] = Field(default_factory=list)
    fixture_file: str | None = None
    target_action: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

class Source(BaseModel):
    source_id: str | None = None
    document_id: int | str | None = None
    filename: str | None = None
    locator: str | None = None
    chunk_index: int | None = None
    similarity: float | None = None

class TargetResponse(BaseModel):
    answer: str = ""
    sources: list[Source] = Field(default_factory=list)
    citation_valid: bool | None = None
    status_code: int = 200
    raw: dict[str, Any] = Field(default_factory=dict)

class Finding(BaseModel):
    detector: str
    passed: bool
    message: str

class CaseResult(BaseModel):
    case_id: str
    category: Category
    severity: str
    passed: bool
    attack_succeeded: bool
    answer: str
    sources: list[Source] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    error: str | None = None
    latency_ms: float | None = None

class RunSummary(BaseModel):
    total: int
    passed: int
    failed: int
    evaluation_errors: int
    attack_success_rate: float
    citation_failure_rate: float
    by_category: dict[str, dict[str, float | int]]
    high_failures: int
    critical_failures: int
    mean_latency_ms: float | None = None
