import json
from pathlib import Path
from typing import Iterable
from pydantic import BaseModel
class JsonlStorage:
    def __init__(self,directory='output'):
        self.directory=Path(directory); self.directory.mkdir(parents=True,exist_ok=True)
    def write(self,records:Iterable[BaseModel],filename):
        path=self.directory/filename
        with path.open('w',encoding='utf-8') as f:
            for record in records:f.write(json.dumps(record.model_dump(mode='json'),ensure_ascii=False)+'\n')
        return path
