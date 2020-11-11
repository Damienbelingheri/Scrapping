import requests
import bs4
import pandas as pd
import sys
import itertools as it 
import random
import time
import csv
import re
from fake_useragent import UserAgent
from urllib.request import urlopen


token = 'https://www.sous-traiter.com/annuaire/liste.php?metier=Usinage,%20M%C3%A9canique&page='


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


def get_data(pages,proxies):

  
    parameters = ['']
    ua = UserAgent()
    proxy_pool = it.cycle(proxies)

    rows = []
    rows.append(['Company Name', 'Webpage', 'Description', 'Location','Email','Phone'])
    #while len(pages) > 0:

    for i in range(0, 2, 1):
        for i in pages:
            #get the url of the page
            response = requests.get(i)


            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            em_box = soup.find_all("a", {"class":"button-reveal"})
            rows = []
            rows.append(['Company Name','CodePostal', 'Location', 'Phone','Email','Website','UrlPage'])
            for result in em_box:

                proxy = next(proxy_pool)
                result = result['href']
                
                
                urlpage = 'https://www.sous-traiter.com/annuaire/'+ result
                
                # query the website and return the html to the variable 'page'
                page = requests.get(urlpage)
                # parse the html using beautiful soup and store in variable 'soup'
                soup = bs4.BeautifulSoup(page.text, 'html.parser')
                # find results within table
                table = soup.find('section',{'id': 'section-infos'})

                # search if the company is premium reaching content
                occurence = soup.find_all('i')
                premium = occurence[4].getText()
                

                data = table.find_all('span')
                a = table.find_all('a',href=True)

                if(premium == 'Premium'):
                    company =  data[0].getText()
                    location = data[1].getText()
                    phone = a[0]['href'].strip('tel:').replace(" ", " ") 
                    email = None
                    website = None
                    codePostal = re.findall(r'\d+', location)[-1]

                else:
                    company =  data[0].getText()
                    location = data[2].getText() +" "+ data[3].getText() + " " + data[4].getText()
                    phone = a[0]['href'].strip('tel:').replace(" ", " ")
                    # fax = data[6].getText()
                    email = a[2].getText()
                    codePostal= data[3].getText()
                    try:
                        website= a[3]['href']
                    except:
                        website = 'none'


                # loop over results


                rows.append([company,codePostal,location, phone,email, website,urlpage])
                print(rows)
           
    with open('usinage-mecanique.csv','a', newline='') as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)
            
    
data = get_data(pages,proxies)
