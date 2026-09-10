# GraphOne Intelligence Graph — AI Engineer Demo Task

Production-oriented reference implementation for the GraphOne / FrontierAtlas AI Engineer demo task.

## What is implemented

- **Phase I:** asynchronous bulk ingestion architecture for startups, products, and research papers; concurrency limits, retries, pagination and GitHub-star enrichment.
- **Phase II:** five configurable AI news sources and five AI job boards, full-text extraction, publication-date normalization and strict 24-hour freshness filtering.
- **Phase III:** multi-tier LLM extraction (Gemini Flash → Groq Llama → DeepSeek), semantic chunking/truncation, 429 exponential backoff + jitter and 413-aware payload sizing.
- **Phase IV:** deterministic startup/product canonicalization against a seed list, with auditable raw-to-canonical mappings.
- **Phase V:** asynchronous `aiohttp` crawling plus a Playwright escalation path for JavaScript/anti-bot sources. The project does not attempt to defeat CAPTCHAs; it documents compliant escalation/fallback behavior.
- **Phase VI:** scalable architecture and storage design for 500k+ records.

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── .env.example
├── architecture.pdf
├── docs/
│   ├── architecture.md
│   └── data-contracts.md
├── src/
│   ├── config.py
│   ├── models.py
│   ├── http_client.py
│   ├── dates.py
│   ├── chunking.py
│   ├── llm.py
│   ├── resolver.py
│   ├── extractors.py
│   ├── sources.py
│   ├── storage.py
│   └── pipeline.py
├── tests/
│   ├── test_dates.py
│   ├── test_chunking.py
│   └── test_resolver.py
└── data/
    └── README.md
```

## Setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

Add provider keys only for the LLM providers you intend to use. The pipeline is designed so missing providers can be skipped rather than causing the entire run to fail.

## Run

```bash
python -m src.pipeline --hours 24 --concurrency 40
```

The implementation is source-config driven: scaling from a trial run to hundreds of thousands of records is achieved by increasing worker count, queue partitions and infrastructure capacity rather than rewriting extraction logic.

## Data quality / anti-hallucination rule

Every canonical record contains source metadata. LLMs are used only to structure retrieved source text; they are not treated as a source of facts. Records without a legitimate source URL are rejected. This is important because the assessment explicitly warns that hallucinated data results in disqualification.

## Expected canonical records

The pipeline models the required fields for STARTUP, PRODUCT, RESEARCH_PAPER and JOB records. News records use the same envelope and add a `NEWS` record type so the six requested output tabs can be produced.

The Google Sheet deliverable is intentionally generated from the pipeline output rather than committed with invented records. Run the export against live sources, review the provenance, then publish the resulting six tabs.

## 500k+ scale design

1. Discovery queues partition work by source and entity type.
2. Async HTTP workers fetch pages with bounded concurrency.
3. A durable queue (Kafka/SQS in production) separates fetching from extraction.
4. Raw HTML is stored immutably in object storage.
5. Normalized records are upserted into PostgreSQL.
6. Redis provides short-lived dedupe/rate-limit state.
7. A graph store (Neo4j/Neptune) models startup-product-paper-job relationships.
8. Vector search is optional and used for semantic similarity, not as the system of record.
9. Metrics/logging expose throughput, 429/413 rates, freshness lag and extraction failures.

## Testing

```bash
pytest -q
```

## Important scope note

This repository is an engineering implementation/template for the 3-day assessment. It does **not** claim that 1,000+ live records or a public Google Sheet were already produced at commit time. Those outputs require running the crawler against the selected live sources and publishing the resulting verified data.
