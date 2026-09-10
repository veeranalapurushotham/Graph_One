from src.resolver import EntityResolver
def test_openai_resolution():
    r=EntityResolver(['OpenAI']).resolve('OpenAI, Inc.')
    assert r.canonical=='OpenAI'
