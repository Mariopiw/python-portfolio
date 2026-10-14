import time
import uuid

import httpx

from harness.models import AttackCase, TargetResponse
from harness.targets.base import TargetAdapter

class OrchestratorHttpTarget(TargetAdapter):
    def __init__(self, config: dict):
        self.base_url = config["base_url"].rstrip("/")
        self.timeout = float(config["timeout_seconds"])
        self.create_path = config["orchestrator"]["create_path"]

        self.headers: dict[str, str] = {}
        bearer = config["auth"].get("bearer_token") or ""
        api_key = config["auth"].get("api_key") or ""

        if bearer:
            self.headers["Authorization"] = f"Bearer {bearer}"
        if api_key:
            self.headers["X-API-Key"] = api_key

    def prepare_case(self, case: AttackCase) -> None:
        return

    def execute(self, case: AttackCase) -> TargetResponse:
        if case.target_action != "submit_unapproved_high_risk":
            raise RuntimeError(f"Unsupported action: {case.target_action}")

        payload = {
            "case_reference": f"RT-{uuid.uuid4()}",
            "description": case.prompt or "Synthetic evaluation test",
            "input_payload": {"red_team": True},
        }

        headers = dict(self.headers)
        headers["Idempotency-Key"] = f"rt-{uuid.uuid4()}"

        started = time.perf_counter()
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}{self.create_path}",
                headers=headers,
                json=payload,
            )
        elapsed = (time.perf_counter() - started) * 1000

        try:
            data = response.json()
        except Exception:
            data = {"text": response.text}

        return TargetResponse(
            answer=str(data.get("status", response.status_code)),
            status_code=response.status_code,
            raw={**data, "_latency_ms": elapsed},
        )
