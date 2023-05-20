#!/usr/bin/python3
import re
import argparse
import requests
import json
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()
parser.add_argument('--url','-u', type=str, nargs='?', const='url', help='URL to RVUSA page')
parser.add_argument('--path','-p', type=str, nargs='?', const='path', default="./", help='Path to write files')
parser.add_argument('--rvclass','-c', type=str, nargs='?', const='ClassNA', help='Class or RV Type. E.g. ClassA/ ClassC')
args = parser.parse_args()
url=args.url
path=args.path
rvtype=args.rvclass
rebaseurl=re.search("^.+?[^\/:](?=[?\/]|$)", url)
baseurl = rebaseurl.group(0)

response = requests.get(url)
soup = bs(response.text,'html.parser')
modelinfo = []
imglist = []
#Get the year/brand/make/model data
modelullist = soup.find("ul", class_="breadcrumbs")
for li in modelullist.find_all("li"):
	modelinfo.append(li.text)
brand=modelinfo[3].replace('\xa0»\xa0','')
make=modelinfo[4].replace('\xa0»\xa0','')
year=modelinfo[5].replace('\xa0»\xa0','')
model=modelinfo[6].replace('/','')

#Find the brochure URL
brochurediv = soup.find("a", class_="literature-btn")
if brochurediv is not None:
	brochureurl = "https:"+brochurediv['href']
else:
	brochureurl = "NA"
#brochurecontent = requests.get(brochureurl).content
#with open(brochurefilename, 'wb') as f:
	#f.write(brochurecontent)


#Find the model and floorplan images and image URLs
for divimglist in soup.find_all("div", class_="col-sm-4 text-center"):
	for imagelist in divimglist.find_all("img", class_="lazyload"):
		imglist.append("https:"+imagelist['data-src'])
modelimgurl=imglist[0]
floorplanimgurl=imglist[1]

modelimgurldata=requests.get(modelimgurl).content
modelimgfile=path+brand+"-"+make+"-"+model+"-"+year+".jpg"
with open(modelimgfile, 'wb') as f:
	f.write(modelimgurldata)
floorplanimgurldata=requests.get(floorplanimgurl).content
floorplanimgfile=path+brand+"-"+make+"-"+model+"-"+year+"floorplan.jpg"
floorplanimgfile.replace('/','')
with open(floorplanimgfile, 'wb') as f:
		f.write(floorplanimgurldata)
		
modeldata = dict(Year = year, Brand = brand, Make = make, Model = model, Class = rvtype, url = url, floorplanimg = floorplanimgfile, modelphoto = modelimgfile, brochurelink=brochureurl)


for row in soup.find_all("div", class_="col-xs-12 s-row"):
	#print(row.find(class_='col-sm-6 s-label').text+" : "+ row.find(class_='col-sm-6 s-value').text)
	label = row.find(class_='col-sm-6 s-label').text
	value = row.find(class_='col-sm-6 s-value').text
	modeldata.update({label: value})


	
jsonfilename = path+brand+"_"+make+"_"+model+"_"+year+".json"

print("Writing: ",jsonfilename)
json_object = json.dumps(modeldata, indent=4)
with open(jsonfilename, "w") as f:
	f.write(json_object)
