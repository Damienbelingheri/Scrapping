
# import libraries
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import csv
from textwrap import wrap


# specify the url
urlpage = 'https://www.sous-traiter.com/annuaire/societe-sds--sous-traitance-depannages-services--01700-neyron-9535.html'
#urlpage = 'https://www.sous-traiter.com/annuaire/fichequart.php?codeAnnuaire=11162'
# query the website and return the html to the variable 'page'
page = requests.get(urlpage)
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page.text, 'html.parser')
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

    
## Create csv and write rows to output file
with open('techtrack100.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)