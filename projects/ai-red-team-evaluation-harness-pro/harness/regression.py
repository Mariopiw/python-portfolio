import json
from pathlib import Path

def save_baseline(summary, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")

def compare(current, baseline_path, max_overall_increase, max_category_increase, max_citation_increase):
    path = Path(baseline_path)
    if not path.exists():
        return True, ["No baseline exists yet"]

    old = json.loads(path.read_text(encoding="utf-8"))
    problems = []

    if current.attack_success_rate - float(old.get("attack_success_rate", 0)) > max_overall_increase:
        problems.append("Overall ASR regressed")

    if current.citation_failure_rate - float(old.get("citation_failure_rate", 0)) > max_citation_increase:
        problems.append("Citation failure rate regressed")

    old_categories = old.get("by_category", {})
    for category, data in current.by_category.items():
        if category in old_categories:
            before = float(old_categories[category].get("attack_success_rate", 0))
            after = float(data.get("attack_success_rate", 0))
            if after - before > max_category_increase:
                problems.append(f"{category} regressed")

    return not problems, problems
