import json
from pathlib import Path
from typing import Iterable
from pydantic import BaseModel

class JsonlStorage:
    """Deterministic local sink used for verified crawl output and replay/testing."""
    def __init__(self, directory='output'):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def write(self, records: Iterable[BaseModel], filename):
        path = self.directory / filename
        with path.open('w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record.model_dump(mode='json'), ensure_ascii=False) + '\n')
        return path

# Production persistence contract:
# PostgreSQL is the canonical transactional store. The pipeline should upsert by
# a deterministic source/content fingerprint, retain source provenance, and keep
# raw HTML in object storage for audit/reprocessing. This module deliberately
# keeps the local JSONL sink dependency-free for reproducible development/tests;
# credentials and infrastructure should be supplied through deployment config.
