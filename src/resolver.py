import re,unicodedata
from dataclasses import dataclass
def normalize_name(value):
    value=unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode(); value=value.lower().replace('&',' and ')
    value=re.sub(r'\b(incorporated|inc|corp|corporation|ltd|limited|llc|co)\b',' ',value)
    return re.sub(r'[^a-z0-9]+',' ',value).strip()
@dataclass
class Resolution:
    raw:str; canonical:str; method:str
class EntityResolver:
    def __init__(self,seed_entities):self.seed={normalize_name(x):x for x in seed_entities}
    def resolve(self,raw):
        key=normalize_name(raw)
        if key in self.seed:return Resolution(raw,self.seed[key],'exact_normalized')
        tokens=set(key.split())
        for norm,canonical in self.seed.items():
            candidate=set(norm.split())
            if tokens and (tokens==candidate or tokens<candidate or candidate<tokens):return Resolution(raw,canonical,'token_subset')
        return Resolution(raw,raw.strip(),'unmatched')
DEFAULT_SEED=['OpenAI','Anthropic','Google DeepMind','Meta AI','Mistral AI','Cohere','Hugging Face','Stability AI','Perplexity','Scale AI']
