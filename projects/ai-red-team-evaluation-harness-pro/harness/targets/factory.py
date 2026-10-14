from harness.targets.orchestrator_http import OrchestratorHttpTarget
from harness.targets.rag_http import SecureRagHttpTarget

def build_target(config: dict):
    kind = config["target"]["kind"]

    if kind == "secure_rag_http":
        return SecureRagHttpTarget(
            config["target"],
            allow_fixture_uploads=bool(config["run"].get("allow_fixture_uploads", False)),
        )

    if kind == "orchestrator_http":
        return OrchestratorHttpTarget(config["target"])

    raise ValueError(f"Unsupported target kind: {kind}")
