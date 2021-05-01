from urllib.request import urlopen
from urllib.parse import unquote
from urllib.error import HTTPError
from bs4 import BeautifulSoup


#Search Wikipedia article and extract text
def search_web(keyword):
    #Get and Load Wikipage
    urlStr = 'https://de.wikipedia.org/wiki/' + keyword
    links = []
    count = 0
    text = ''
    
    #handle empty pages
    try:
        html_page = urlopen(urlStr).read()
    except HTTPError:
        return 'Zu diesem Thema gibt es keinen Wikipedia Artikel', []

    soup = BeautifulSoup(html_page, features="html.parser")

    #remove tables first (so no text from tables is taken)
    for table in soup.find_all("table"):
        table.decompose()

    #Get first few lines
    for i in soup.find_all('p'):
        if count < 2:
            text += i.getText()
            count += 1
    
    #Remove irrelevant symbols
    for ch in ['\n', '?/i', '\xa0', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]', '[10]', '[11]', '[12]']:
        if ch in text:
            text = text.replace(ch, '')
    '''
    #Case: empty article
    if 'Artikel verschwunden?' in text:
        return 'Zu diesem Thema gibt es keinen Wikipedia Artikel', []
    '''

    #Case: multiple articles
    if len(text) < 130:
        text = 'Zu diesem Thema gibt es keinen Wikipedia Artikel'
        f = open(keyword + ".txt", "w", encoding='utf-8')
        f.write("Meinst du vielleicht eine der folgenden Optionen:" + '\n')
        count = 1

        #mw-content-text
        for link in soup.find_all("a"):
            url = link.get("href", "")
            if "wiktionary" in url:
                break
            if 'Wikipedia:Begriffskl%C3%A4rung' in url:
                break
            if "/wiki/" in url:
                name = url.removeprefix('/wiki/')
                links.append(name)
                enc_name = unquote(name)
                enc_name = enc_name.replace('_', ' ')
                f.write(str(count) + ". " + enc_name + '\n')
                count += 1
        f.close()

    if len(text) > 2000:
        text = text[:2000]

    return text, links