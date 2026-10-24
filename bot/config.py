from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    public_key: str
    secret_key: str
    dry_run: bool
    currency: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        public = os.getenv("BAYSE_PUBLIC_KEY", "pk_live_MXANgNN4yGLurORxVNC-lNX4")
        secret = os.getenv("BAYSE_SECRET_KEY", "")

        if not secret or secret.startswith("sk_live_your_"):
            raise ValueError(
                "BAYSE_SECRET_KEY is missing. "
                "Copy .env.example to .env and put your real secret key."
            )

        return cls(
            public_key=public,
            secret_key=secret,
            dry_run=os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes"),
            currency=os.getenv("CURRENCY", "NGN").upper(),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


settings = Settings.from_env()