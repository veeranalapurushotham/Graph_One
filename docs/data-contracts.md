# Data contracts

The implementation follows the task's required envelope: `schemaVersion`, `recordType`, `source.name`, `source.url`, and `collectedAt`.

## STARTUP
`entityName`; `employeeCount` when available.

## PRODUCT
`startupName`; `pricingModel` in FREE, FREEMIUM, PAID, ENTERPRISE.

## RESEARCH_PAPER
`title`; `authors`; `paper_url`; `github_url` when available; `github_stars`; `published_date`.

## JOB
`company`; `date`; `is_remote`; `role_family`.

## NEWS
`title`; `date`; `content`; `url`.

Every record must retain legitimate provenance. LLM output is treated as a transformation of retrieved source text, not as evidence.
