from pathlib import Path
import time

import httpx

from harness.models import AttackCase, Source, TargetResponse
from harness.targets.base import TargetAdapter

class SecureRagHttpTarget(TargetAdapter):
    def __init__(self, config: dict, allow_fixture_uploads: bool):
        self.base_url = config["base_url"].rstrip("/")
        self.timeout = float(config["timeout_seconds"])
        self.ask_path = config["rag"]["ask_path"]
        self.upload_path = config["rag"]["upload_path"]
        self.allow_fixture_uploads = allow_fixture_uploads

        self.headers: dict[str, str] = {}
        bearer = config["auth"].get("bearer_token") or ""
        api_key = config["auth"].get("api_key") or ""

        if bearer:
            self.headers["Authorization"] = f"Bearer {bearer}"
        if api_key:
            self.headers["X-API-Key"] = api_key

        self._uploaded: set[str] = set()

    def prepare_case(self, case: AttackCase) -> None:
        if not case.fixture_file:
            return

        if not self.allow_fixture_uploads:
            raise RuntimeError(
                f"{case.id} requires fixture upload. "
                "Enable only for owned/authorized targets."
            )

        if case.fixture_file in self._uploaded:
            return

        path = Path(case.fixture_file)
        with httpx.Client(timeout=self.timeout) as client, path.open("rb") as fh:
            response = client.post(
                f"{self.base_url}{self.upload_path}",
                headers=self.headers,
                files={"file": (path.name, fh)},
            )

        if response.status_code not in (200, 201, 409):
            response.raise_for_status()

        self._uploaded.add(case.fixture_file)

    def execute(self, case: AttackCase) -> TargetResponse:
        started = time.perf_counter()

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}{self.ask_path}",
                headers=self.headers,
                json={"question": case.prompt or ""},
            )
            elapsed = (time.perf_counter() - started) * 1000
            response.raise_for_status()
            data = response.json()

        result = TargetResponse(
            answer=str(data.get("answer", "")),
            sources=[Source.model_validate(item) for item in data.get("sources", [])],
            citation_valid=data.get("citation_valid"),
            status_code=response.status_code,
            raw=data,
        )
        result.raw["_latency_ms"] = elapsed
        return result
