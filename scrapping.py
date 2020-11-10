import requests
import bs4
import pandas as pd
import sys
import itertools as it 
import random
import time
import csv
from fake_useragent import UserAgent

token = 'https://www.sous-traiter.com/annuaire/liste.php?metier=Usinage,%20M%C3%A9canique&page='


def get_pages(token, nb):
    pages = []
    for i in range(1,nb+1):
        j = token + str(i)
        pages.append(j)
    return pages 
    
pages = get_pages(token,30)

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
    while len(pages) > 0:
        for i in pages:
            response = requests.get(i)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            em_box = soup.find_all("a", {"class":"button-reveal"})
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
                rows = []
                rows.append(['Company Name', 'Webpage', 'Description', 'Location','Email','Phone'])




                company =  data[0].getText()
                print (company)
                location = data[2].getText() +" "+ data[3].getText() + " " + data[4].getText()
                print (location)
                phone = a[0]['href'].strip('tel:').replace(" ", " ")
                fax = data[6].getText()
                email = a[2].getText() 
                website= data[9].getText()



                # loop over results


                rows.append([company,location, phone, fax,email, website])
                print(rows)

                with open('techtrack100.csv','w', newline='') as f_output:
                    csv_output = csv.writer(f_output)
                    csv_output.writerows(rows)

            sys.exit()


    

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