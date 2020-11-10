import requests
import bs4
import pandas as pd
import sys
import itertools as it 
import random
import time
import csv
from fake_useragent import UserAgent

token = 'https://www.sous-traiter.com/annuaire/liste.php?metier=Usinage,%20M%C3%A9canique&page=56'


def get_pages(token, nb):
    pages = []
    for i in range(1,nb+1):
        j = token + str(i)
        pages.append(j)
    return pages 
    
pages = get_pages(token,1)

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

    rows = []
    rows.append(['Company Name', 'Webpage', 'Description', 'Location','Email','Phone'])

    token = 'https://www.sous-traiter.com/annuaire/liste.php?metier=Usinage,%20M%C3%A9canique&page=29'


    response = requests.get(token)
    print (response.text)


    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    em_box = soup.find_all("a", {"class":"button-reveal"})
    rows = []
    rows.append(['Company Name', 'Location', 'Phone','Email','Website'])
    for result in em_box:
        result = result['href']

        urlpage = 'https://www.sous-traiter.com/annuaire/'+ result
        
        # query the website and return the html to the variable 'page'
        page = requests.get(urlpage)
        # parse the html using beautiful soup and store in variable 'soup'
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        # find results within table
        table = soup.find('section',{'id': 'section-infos'})

        data = table.find_all('span')
        a = table.find_all('a',href=True)
        #print('Number of results', len(results))

        # create and write headers to a list 
        

        company =  data[0].getText()
        location = data[2].getText() +" "+ data[3].getText() + " " + data[4].getText()
        phone = a[0]['href'].strip('tel:').replace(" ", " ")
        # fax = data[6].getText()
        email = a[2].getText() 

        try:
            website= a[3]['href']

        except:
            website = 'none'

        print (website)

        location2 = data[1].getText()
        loc = location2.strip('*').replace(" " ," ")

        # loop over results


        rows.append([company,location, phone,email, website])

        print(rows)
        with open('scrapping.csv','w', newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(rows)
    

data = get_data(pages,proxies)
