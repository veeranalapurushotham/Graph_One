def semantic_chunks(text,max_chars=12000,overlap=600):
    text=' '.join(text.split())
    if len(text)<=max_chars:return [text]
    chunks=[]; start=0
    while start<len(text):
        end=min(len(text),start+max_chars)
        if end<len(text):
            boundary=max(text.rfind('. ',start,end),text.rfind('\n',start,end))
            if boundary>start+max_chars//2:end=boundary+1
        chunks.append(text[start:end].strip())
        if end>=len(text):break
        start=max(0,end-overlap)
    return chunks
