from __future__ import annotations

import os


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "Polyglot Commerce Integration Hub")
        self.environment = os.getenv("APP_ENV", "development")
        self.host = os.getenv("APP_HOST", "0.0.0.0")
        self.port = int(os.getenv("APP_PORT", "8080"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()


settings = Settings()
