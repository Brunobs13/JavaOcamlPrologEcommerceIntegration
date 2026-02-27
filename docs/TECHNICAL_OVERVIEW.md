# Technical Overview

## 1. Deep Architecture Explanation
### End-to-End Flow
1. User interacts with dashboard to build a cart and choose customer.
2. Frontend calls `/api/quote` or `/api/orders`.
3. API validates payload and delegates to `CommerceService`.
4. Service loads rule context (discounts, loyalty, shipping) from Prolog-derived dataset.
5. Quote/order is computed and inventory/metrics are updated.
6. Updated data is returned for immediate UI refresh.

### Key Decisions
- FastAPI selected for lightweight, typed API layer.
- Legacy Java/OCaml/Prolog preserved for traceability in `legacy/`.
- Runtime built around deterministic rule evaluation for reproducibility.

### Trade-offs
- In-memory orders are fast but non-persistent.
- Legacy language code is archived, not executed in runtime path.
- No auth layer yet for public production access.

### Alternatives Considered
- Direct Java runtime API: heavier setup and lower portability.
- Database-first architecture: deferred for faster modernization cycle.

## 2. Junior Interview Questions
- Why keep legacy files in `legacy/`?
- How does Prolog data feed the API?
- What is the difference between quote and order endpoints?
- How are discounts and loyalty computed?
- Why use environment variables?

## 3. Senior Interview Questions
- How would you introduce durable storage and idempotency?
- How would you design a safe migration from in-memory to DB transactions?
- How would you scale this service for high-throughput checkout flows?
- How would you enforce governance for multi-language business rules?
- How would you secure and audit all operations end-to-end?

## 4. Critical Code Sections
### `core/data.py -> load_prolog_dataset`
Parses legacy Prolog facts into typed dataset structures consumed by runtime services.

### `engine/service.py -> _build_quote`
Core financial logic: subtotal, category discounts, loyalty discounts, shipping, and final total.

### `engine/service.py -> create_order`
Commits transactional behavior in memory (inventory mutation + order history + metrics).

### `api/app.py`
Defines service contract and centralizes request validation/error mapping.

### `api/static/app.js`
Implements operational UI orchestration with cart lifecycle and API synchronization.

## 5. Scaling Discussion
- Persist orders/inventory in PostgreSQL.
- Add background workers for asynchronous tasks.
- Add caching for static catalog data.
- Add distributed tracing and SLA instrumentation.

## 6. Memory Management Discussion
- Memory growth driven by order history and inventory map.
- Introduce history retention policies and persistence offloading for long-lived workloads.

## 7. Concurrency Discussion
- Current implementation is single-process and request-driven.
- Production extension should include transaction-safe persistence and optimistic locking semantics.
