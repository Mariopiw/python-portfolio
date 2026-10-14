import os
import re
from pathlib import Path
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")

class Settings(BaseSettings):
    target_kind: str = "secure_rag_http"
    target_base_url: str = "http://localhost:8000"
    target_bearer_token: str = ""
    target_api_key: str = ""
    target_timeout_seconds: int = 120
    canary_secret: str = "ACME_CANARY_7F3A_DO_NOT_REVEAL"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

def _expand(value):
    if isinstance(value, str):
        return ENV_PATTERN.sub(lambda m: os.getenv(m.group(1), m.group(0)), value)
    if isinstance(value, list):
        return [_expand(v) for v in value]
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    return value

def load_config(path: str = "config.yaml") -> dict:
    data = _expand(yaml.safe_load(Path(path).read_text(encoding="utf-8")))
    t = data["target"]
    defaults = {
        "kind": settings.target_kind,
        "base_url": settings.target_base_url,
        "timeout_seconds": settings.target_timeout_seconds,
    }
    for key, default in defaults.items():
        if isinstance(t.get(key), str) and t[key].startswith("${"):
            t[key] = default
    auth = t["auth"]
    if isinstance(auth["bearer_token"], str) and auth["bearer_token"].startswith("${"):
        auth["bearer_token"] = settings.target_bearer_token
    if isinstance(auth["api_key"], str) and auth["api_key"].startswith("${"):
        auth["api_key"] = settings.target_api_key
    t["timeout_seconds"] = int(t["timeout_seconds"])
    return data
