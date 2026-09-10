from src.chunking import semantic_chunks
def test_chunking_respects_limit():
    chunks=semantic_chunks('word '*5000,max_chars=1000,overlap=50)
    assert chunks
    assert max(map(len,chunks))<=1000
