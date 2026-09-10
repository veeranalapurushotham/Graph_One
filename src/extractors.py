from bs4 import BeautifulSoup
def extract_main_text(html):
    soup=BeautifulSoup(html,'html.parser')
    for node in soup(['script','style','noscript','svg']):node.decompose()
    main=soup.find('main') or soup.find('article') or soup.body or soup
    return ' '.join(main.stripped_strings)
def meta_date(html):
    soup=BeautifulSoup(html,'html.parser')
    for key in ('article:published_time','datePublished','pubdate','date'):
        tag=soup.find('meta',attrs={'property':key}) or soup.find('meta',attrs={'name':key})
        if tag and tag.get('content'):return tag['content']
    return None
