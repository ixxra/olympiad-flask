from urllib import request
from json import loads

def content(title):
    '''
    content(title)

    extracts wikipedia content based on the article's title

    Parameter:
        title - Article's title url escaped.

    Returns:

        title - The article's title formated.
        html  - Article's content as html.
    '''
    req = request.urlopen('http://en.wikipedia.org/w/api.php?format=json&action=query&titles={title}&prop=revisions&rvprop=content&rvparse'.format(title=title))
    data = req.readall()
    d = loads(data.decode())
    pages = d['query']['pages']
    desc, content = pages.popitem()
    title = content['title']
    rev = content['revisions'].pop()
    html = rev['*']
    return title, html
