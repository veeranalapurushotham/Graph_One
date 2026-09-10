# GraphOne / FrontierAtlas — AI Engineer Demo Task

## Status
This repository contains the implementation scaffold and architecture for the six-phase AI Engineer demo task. It is **not a fabricated-data submission**. Live datasets must be produced from verified sources before claiming the acceptance criteria are complete.

## Deliverables in this repository
- `docs/architecture.pdf` — architecture deliverable
- `docs/architecture.md` — architecture details
- `docs/data-contracts.md` — structured data contracts
- `src/` — async ingestion, date/freshness, chunking, LLM orchestration, resolution and pipeline modules
- `tests/` — unit tests for dates, chunking and entity resolution
- `data/README.md` — data output guidance

## Required final outputs before submission
1. Verified startup records (target: 1,000+)
2. Verified product records (target: 1,000+)
3. Verified research-paper records (target: 1,000+)
4. Fresh AI news records from the required sources
5. Fresh AI job records from the required sources
6. Source URLs/provenance for collected records
7. GitHub URL/star enrichment where required
8. Entity-resolution output and logs
9. End-to-end execution/test evidence
10. Required Google Sheet containing the verified outputs

**No placeholder or hallucinated records should be presented as real task output.**

## Architecture
The design uses source/vertical partitioning, durable queues, asynchronous HTTP workers, raw-object preservation, PostgreSQL as the canonical store, Redis for short-lived dedupe/rate-limit state, and graph storage for relationships. The architecture also defines 413 chunking, 429 backoff/jitter, freshness handling, Playwright escalation, CAPTCHA-safe behavior and observability.

## LLM fallback
Required order: Gemini Flash → Groq Llama 3 → DeepSeek. Provider responses must be real and verified; this repository does not fabricate provider output.

## Running
Create a virtual environment, install `requirements.txt`, copy `.env.example` to `.env`, configure the required provider/source credentials, then run the pipeline according to the source-specific configuration. Do not publish results until URLs, timestamps and extracted fields have been verified.
