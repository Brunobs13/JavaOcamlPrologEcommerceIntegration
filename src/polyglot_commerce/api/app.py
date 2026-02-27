from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ..core.data import dataset_from_legacy, load_prolog_dataset
from ..core.models import CartLine
from ..engine.service import CommerceService
from ..utils.logging import configure_logging
from ..utils.settings import settings
from .schemas import QuoteRequest

configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[3]
STATIC_DIR = Path(__file__).resolve().parent / "static"
PROLOG_FILE = Path(
    __import__("os").getenv("PROLOG_DATA_FILE", str(ROOT / "legacy" / "academic_project" / "store.pl"))
)

try:
    DATASET = load_prolog_dataset(PROLOG_FILE)
except Exception as error:  # pragma: no cover - startup fallback
    logger.warning("failed loading configured Prolog file: %s", error)
    DATASET = dataset_from_legacy()

SERVICE = CommerceService(DATASET)

app = FastAPI(
    title="Polyglot Commerce Integration Hub",
    version="2.0.0",
    description="Professional e-commerce integration platform based on Java + OCaml + Prolog legacy assets.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=str(STATIC_DIR)), name="assets")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> Dict[str, str]:
    return SERVICE.health()


@app.get("/api/integration")
def integration() -> dict:
    return SERVICE.integration_status(ROOT)


@app.get("/api/customers")
def customers() -> dict:
    return {"customers": SERVICE.list_customers()}


@app.get("/api/items")
def items() -> dict:
    return {"items": SERVICE.list_products()}


@app.get("/api/orders")
def orders() -> dict:
    return {"orders": SERVICE.list_orders()}


@app.get("/api/metrics")
def metrics() -> dict:
    return SERVICE.metrics()


@app.get("/api/dashboard")
def dashboard() -> dict:
    return SERVICE.dashboard(ROOT)


@app.post("/api/quote")
def quote(payload: QuoteRequest) -> dict:
    try:
        lines = [CartLine(item_id=line.item_id, quantity=line.quantity) for line in payload.lines]
        return SERVICE.quote(payload.customer_id, lines)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/orders")
def order(payload: QuoteRequest) -> dict:
    try:
        lines = [CartLine(item_id=line.item_id, quantity=line.quantity) for line in payload.lines]
        return SERVICE.create_order(payload.customer_id, lines)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/reset")
def reset() -> dict:
    return SERVICE.reset()
