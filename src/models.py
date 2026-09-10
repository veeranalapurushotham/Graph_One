from datetime import datetime
from typing import Literal, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
RecordType=Literal['STARTUP','PRODUCT','RESEARCH_PAPER','JOB','NEWS']
class Source(BaseModel):
    name:str
    url:HttpUrl
class Envelope(BaseModel):
    model_config=ConfigDict(extra='forbid')
    schemaVersion:str='1.0'
    recordType:RecordType
    source:Source
    collectedAt:datetime
class StartupRecord(Envelope):
    recordType:Literal['STARTUP']='STARTUP'
    entityName:str
    employeeCount:int|None=None
class ProductRecord(Envelope):
    recordType:Literal['PRODUCT']='PRODUCT'
    startupName:str|None=None
    pricingModel:Literal['FREE','FREEMIUM','PAID','ENTERPRISE']|None=None
class ResearchPaperRecord(Envelope):
    recordType:Literal['RESEARCH_PAPER']='RESEARCH_PAPER'
    title:str
    authors:list[str]=Field(default_factory=list)
    paper_url:HttpUrl
    github_url:HttpUrl|None=None
    github_stars:int|None=None
    published_date:datetime
class JobRecord(Envelope):
    recordType:Literal['JOB']='JOB'
    company:str
    date:datetime
    is_remote:bool=False
    role_family:str
class NewsRecord(Envelope):
    recordType:Literal['NEWS']='NEWS'
    title:str
    date:datetime
    content:str
    url:HttpUrl
    extra:dict[str,Any]=Field(default_factory=dict)
