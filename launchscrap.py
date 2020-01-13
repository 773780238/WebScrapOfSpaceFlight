# -*- coding: utf-8 -*-

import datetime
import re
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
begin = datetime.datetime(2019,1,1,0,0)
end = datetime.datetime(2020,1,1,0,0)
d = begin
delta = datetime.timedelta(days = 1)
m_hashmap = {}
#initiate the hashmap of (date -> value)
while d <= end:
    m_hashmap[d] = 0
    #print(d.astimezone().isoformat())
    d += delta
    
html = urlopen("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches")
bsObj = BeautifulSoup(html.read(),  "html.parser" )
#locate the table of interest
table = bsObj.find_all('table')[3]
target = None
#iterate through tr and td
for table_row in table.findAll('tr'):
    #decide if we need to change target date
    if table_row.find(text=re.compile('[0-9]+ (January|February|March|April|May|June|July|August|September|October|November|December)')) and table_row.get('style') is None:
        text = table_row.find(text=re.compile('[0-9]+ (January|February|March|April|May|June|July|August|September|October|November|December)'))
        #if not found or text is invalid, pass 
        if text is None or len(text)>15:
            continue
        text = str(text)+" 2019"
        target = datetime.datetime.strptime(text, '%d %B %Y')
    #get td in the tr    
    columns = table_row.findAll('td') 
    if target is None:
        continue
    for column in columns:
        #if launch success, add 1 to target date in the hashmap
        if column.find_all(text=re.compile('Operational|Successful|En route')):
            m_hashmap[target] += 1
#write the output to the csv
f = open("output.csv", "w", newline="")
writer = csv.writer(f)

for k,v in m_hashmap.items():
    writer.writerow([k.astimezone().isoformat(), v])

f.close() 
    