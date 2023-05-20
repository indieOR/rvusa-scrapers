#!/usr/bin/python3

import argparse
import requests
import json
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()
parser.add_argument('--year', '-y', type=str, nargs='?', const='year', help='Model year 4-digits, e.g. 2021')
parser.add_argument('--brand','-b', type=str, nargs='?', const='brand', help='Brand, e.g. Winnebago')
parser.add_argument('--make','-m', type=str, nargs='?', const='make', help='Make, e.g. Vista')
parser.add_argument('--model','-M', type=str, nargs='?', const='model', help='Model Name, e.g. 35F ')
parser.add_argument('--url','-u', type=str, nargs='?', const='url', help='URL to RVUSA page')
args = parser.parse_args()
url=args.url
year=args.year
brand=args.brand
make=args.make
model=args.model

response = requests.get(url)
soup = bs(response.text,'html.parser')
specsdict = {}
modelinfo = []

#Get the year/make/model
ullist = soup.find("ul", class_="breadcrumbs")
for li in ullist.find_all("li"):
	modelinfo.append(li.text)
	#print("Data:"+li.text)
brand=modelinfo[3].replace('\xa0»\xa0','')
make=modelinfo[4].replace('\xa0»\xa0','')
year=modelinfo[5].replace('\xa0»\xa0','')
model=modelinfo[6]
print(year,brand,make,model)

for row in soup.find_all("div", class_="col-xs-12 s-row"):
	#print(row.find(class_='col-sm-6 s-label').text+" : "+ row.find(class_='col-sm-6 s-value').text)
	label = row.find(class_='col-sm-6 s-label').text
	value = row.find(class_='col-sm-6 s-value').text
	specsdict.update({label: value})
	#divs = row.find_all("div")
	#attr_name = divs[0].get_text().strip()
	#attr_value = divs[1].get_text().strip()
	#print(f"{attr_name} = {attr_value}")
	
#Write json to a file
filename = brand+"-"+make+"-"+model+"-"+year+".json"
json_object = json.dumps(specsdict, indent=4)
with open(filename, "w") as outfile:
	outfile.write(json_object)
