# GraphOne Architecture — concise technical design

## 1. 500k+ scale strategy
Use a durable queue partitioned by vertical and source. Discovery creates normalized work items; asynchronous fetch workers consume them with per-domain concurrency limits. Raw responses go to object storage, while normalized entities go to PostgreSQL. Horizontal scaling means adding worker replicas and queue partitions, not changing extraction code.

A production deployment can use Kafka/SQS, object storage, PostgreSQL, Redis and a graph database such as Neo4j/Neptune. Kubernetes or ECS can autoscale workers from queue depth.

## 2. 413 and 429 handling
**413:** extract the main article body, remove navigation/boilerplate, split text at semantic sentence boundaries and use bounded overlap. Never blindly send an entire HTML document to an LLM.

**429:** honor `Retry-After` when supplied, otherwise use exponential backoff with jitter. Apply provider-specific concurrency budgets and a circuit breaker so one failing provider does not stall the queue.

Fallback order: Gemini Flash → Groq Llama 3 → DeepSeek.

## 3. Freshness and duplicate prevention
Normalize publication dates into UTC. Relative dates such as “2 hours ago” are resolved against the crawl timestamp. Reject records older than 24 hours. For sources without trustworthy dates, keep a source fingerprint plus last-seen timestamp and only accept content whose fingerprint is new.

Use a durable uniqueness key such as `sha256(source_url + canonical_content_hash)` for distributed deduplication. PostgreSQL unique constraints make the final write idempotent.

## 4. Storage
PostgreSQL is the primary system of record because it provides transactions, constraints, upserts and operational maturity. Object storage keeps raw HTML for audit/reprocessing. A graph database models relationships such as startup → product, paper → GitHub repository and company → job. A vector store is optional for semantic retrieval and similarity; it is not the authoritative store.

## Anti-bot / JavaScript-heavy domains
Start with compliant HTTP retrieval. If a source is JavaScript-rendered, use Playwright Async in a controlled worker pool. Respect robots.txt, terms of service, rate limits and access restrictions. Do not attempt CAPTCHA solving or bypass access controls. If a domain actively blocks automation, use an allowed API/feed or document the source as unavailable rather than manufacturing data.

## Observability
Emit structured logs and metrics for fetch latency, HTTP status, retries, 413/429 counts, parsing failures, freshness lag, records accepted/rejected, provider fallback count and dedupe rate.
