from dataclasses import dataclass
@dataclass(frozen=True)
class SourceConfig:
    name:str; url:str; kind:str
NEWS_SOURCES=[SourceConfig('TechCrunch AI','https://techcrunch.com/category/artificial-intelligence/','news'),SourceConfig('VentureBeat AI','https://venturebeat.com/category/ai/','news'),SourceConfig('MIT Technology Review AI','https://www.technologyreview.com/topic/artificial-intelligence/','news'),SourceConfig('The Decoder','https://the-decoder.com/','news'),SourceConfig('AI News','https://www.artificialintelligence-news.com/','news')]
JOB_SOURCES=[SourceConfig('LinkedIn AI Jobs','https://www.linkedin.com/jobs/','jobs'),SourceConfig('Indeed AI Jobs','https://www.indeed.com/q-artificial-intelligence-jobs.html','jobs'),SourceConfig('Wellfound','https://wellfound.com/jobs','jobs'),SourceConfig('Built In AI Jobs','https://builtin.com/artificial-intelligence/jobs','jobs'),SourceConfig('AI-Jobs.net','https://ai-jobs.net/','jobs')]
PAPER_SOURCES=[SourceConfig('arXiv','https://arxiv.org/list/cs.AI/recent','papers'),SourceConfig('Papers with Code','https://paperswithcode.com/','papers')]
