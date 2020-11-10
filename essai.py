
# import libraries
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import csv
from textwrap import wrap
import re


# specify the url
urlpage = 'https://www.sous-traiter.com/annuaire/societe-ryg-95100-argenteuil-2888.html'
urlpage = 'https://www.sous-traiter.com/annuaire/fichequart.php?codeAnnuaire=11162'
# query the website and return the html to the variable 'page'
page = requests.get(urlpage)
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page.text, 'html.parser')
# find results within table
table = soup.find('section',{'id': 'section-infos'})

# search if the company is premium reaching content
title = soup.find_all('i')
print (title[4].getText())

data = table.find_all('span')
a = table.find_all('a',href=True)

#print('Number of results', len(results))

# create and write headers to a list 
rows = []
rows.append(['Company Name','CodePostal', 'Location', 'Phone','Email','Website','UrlPage'])

if(title[4].getText() == 'Premium'):
    #print('nique ta mère')
    company =  data[0].getText()
    location = data[1].getText()
    phone = a[0]['href'].strip('tel:').replace(" ", " ") 
    email = None
    website = None
    codePostal = re.findall(r'\d+', location)[-1]


    
    #print (company,location,phone,website)

else:


    company =  data[0].getText()
    location = data[2].getText() +" "+ data[3].getText() + " " + data[4].getText()
    phone = a[0]['href'].strip('tel:').replace(" ", " ")
    #fax = data[6].getText()
    email = a[2].getText() 
    codePostal= data[3].getText()
    #print(website)


# loop over results

rows.append([company,codePostal,location, phone,email, website])
#print(rows)

    
## Create csv and write rows to output file
with open('techtrack100.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)