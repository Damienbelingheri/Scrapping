import requests
import bs4
import pandas as pd
import sys
import itertools as it 
import random
import time
from fake_useragent import UserAgent

token = 'https://www.sous-traiter.com/annuaire/liste.php?metier=Usinage,%20M%C3%A9canique&page=1'


def get_pages(token, nb):
    pages = []
    for i in range(1,nb+1):
        j = token + str(i)
        pages.append(j)
    return pages 
    
pages = get_pages(token,295)



proxies = pd.read_csv('proxy_list.txt', header = None)
proxies = proxies.values.tolist()
proxies = list(it.chain.from_iterable(proxies))
proxy_pool = it.cycle(proxies)
proxy = next(proxy_pool)

def get_data(pages,proxies):

    df = pd.DataFrame()
    parameters = ['']
    ua = UserAgent()
    proxy_pool = it.cycle(proxies)

    while len(pages) > 0:
        for i in pages:
            response = requests.get(i)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            em_box = soup.find("a", {"class":"button-reveal"})
            result = em_box['href']

            token2 = 'https://www.sous-traiter.com/annuaire/'+ result
            # print (token)
            token2 = 'https://www.sous-traiter.com/annuaire/societe-sds--sous-traitance-depannages-services--01700-neyron-9535.html'
            responsePage = requests.get(token2)
            soup2 = bs4.BeautifulSoup(responsePage.text, 'html.parser')
            em_box2 = soup2.find("section", {"id":"section-infos"})
            # print(em_box2.findAll("span",{"class":"subtitle"}))

            parameters = ['href[mailto]', 'href[tel]']
            df_f = pd.DataFrame()
            for par in parameters:
                l = []
                for el in em_box2:
                    print (par)
                    sys.exit()
                    j = el[par]
                    l.append(j)
                l = pd.DataFrame(l, columns = [par])
                df_f = pd.concat([df_f,l], axis = 1)
            sys.exit()
                        

data = get_data(pages,proxies)

