from __future__ import annotations

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='{"ts":"%(asctime)s","level":"%(levelname)s","component":"polyglot-commerce-api","msg":"%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        stream=sys.stdout,
    )
