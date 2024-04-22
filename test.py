import requests
from bs4 import BeautifulSoup


def search(inp):
    for i in ["how does","google"]:
        if i in inp:
            if i == "how does":
                sPoint = inp.find(i) + 1
            else:
                sPoint = inp.find(i) + len(i) + 1
            data = inp[sPoint:]
            #webbrowser.open("https://www.google.com/search?client=firefox-b-d&q="+data)  : client end
            params = {
                "q": data,      	# query example
                "hl": "sv",      	# language
                "gl": "se",      	# country of the search, UK -> United Kingdom
                "start": 0,      	# number page by default up to 0
                #"num": 100      	# parameter defines the maximum number of results to return.
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            info = []
            html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
            soup = BeautifulSoup(html.text, 'lxml')
            try:
                snippet = soup.select_one(".hgKElc").text
            except:
                try:
                    snippet = soup.select_one(".lEBKkf span").text
                except:
                    snippet = None
            print (snippet)
            return({"Search" : ["https://www.google.com/search?client=firefox-b-d&q="+data, snippet]})

print(search("google a apple recipy"))