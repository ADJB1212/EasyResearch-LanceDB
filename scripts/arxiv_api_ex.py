import requests
import feedparser

def api_call():
    #base enedpoint is http://export.arxiv.org/api/query
    #search_query=cat:cs.LG -> search for papers in category cs.LG
    #start at 0 (beginning)
    #max_results 10 
    #sortBy=submittedDate (sort results by submission date)
    #sortOrder=descending (show newest papers first)
    query_url = '''http://export.arxiv.org/api/query?
    search_query=cat:cs.LG&
    start=0&
    max_results=10&
    sortBy=submittedDate&
    sortOrder=descending'''

    response = requests.get(query_url)

    feed = feedparser.parse(response.text)

    return feed