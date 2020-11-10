import requests
import bs4
import pandas as pd
import sys
import itertools as it 
import random
import time
from fake_useragent import UserAgent
import urllib.request
import csv

token = 'https://www.sous-traiter.com/annuaire/liste.php?metier=Usinage,%20M%C3%A9canique&page='


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


    #token2 = 'https://www.sous-traiter.com/annuaire/'+ result
    # print (token)
    token2 = 'https://www.sous-traiter.com/annuaire/societe-sds--sous-traitance-depannages-services--01700-neyron-9535.html'
    responsePage = requests.get(token2)
    soup2 = bs4.BeautifulSoup(responsePage.text, 'html.parser')
    #print (soup2)
    em_box2 = soup2.find("section", {"id":"section-infos"})
    #print(em_box2.find_all('h3'))
    print(em_box2)
    sys.exit()
    results = em_box2.find_all('div')
    company_name = em_box2.find('h3')
    rows = [] 
    rows.append(['Company Name', 'Webpage','Location', 'Telephone', 'Email'])
    #print(rows)
    for result in results:
        data1 = result.find('div')
        print (data1[0].getText)
        if len(data1) == 0:
            continue
        #print (data)
    sys.exit()

    # print(em_box2.findAll("span",{"class":"subtitle"}))
    print(em_box2.find('a', {'href'}))
    print('Number of results', len(em_box2))
    parameters = ['href[mailto]', 'href[tel]']
    df_f = pd.DataFrame()
    # for par in parameters:
    #     l = []
    #     for el in em_boxse2:
    #         print (par)
    #         sys.exit()
    #         j = el[par]
    #         l.append(j)
    #     l = pd.DataFrame(l, columns = [par])
    #     df_f = pd.concat([df_f,l], axis = 1)
    #     print (l,df_f)
    # sys.exit()
                

data = get_data(pages,proxies)

	#	 <div class="toggle fiche" id="email">
	#	<div class="togglet"><i class="toggle-closed icon-ok-circle"></i><i class="toggle-open icon-remove-circle"></i>AFFICHER L'EMAIL</div>
	# <div class="togglec" style="display: none;"><span class="subtitle"><a href="mailto:curty@curty-precision.com"><span itemprop="email">curty@curty-precision.com</span></a></span></div>
	#<span itemprop="streetAddress">425 Route du Cammas</span><br/><span itemprop="postalCode">
    #46110</span> <span itemprop="addressLocality">VAYRAC</span></span></h3>				 


    #<div class="fbox-icon" data-animate="bounceIn">
	#<i class="icon-map-marker2"></i>
	#</div>
	#<h3>Siège social<span class="subtitle">23, Avenue Ampère<br />
    #ZI de Villemilan<br/>91320 WISSOUS</span></h3>