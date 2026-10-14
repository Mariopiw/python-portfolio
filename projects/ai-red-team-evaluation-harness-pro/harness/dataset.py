import json
from pathlib import Path
from harness.models import AttackCase

def load_cases(dataset_dir: str, categories: list[str]) -> list[AttackCase]:
    cases = []
    for category in categories:
        path = Path(dataset_dir) / f"{category}.jsonl"
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                cases.append(AttackCase.model_validate(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"{path}:{lineno}: {exc}") from exc
    return cases
