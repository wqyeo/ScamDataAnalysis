import json
import requests
from bs4 import BeautifulSoup

with open('..\\debug.json') as f:# file path of jason
    data = json.load(f)# input json file to data

for Stories in data['Stories']:
    r = requests.get('https://www.scamalert.sg/'+Stories['Url']).content
    soup = BeautifulSoup(r,'html.parser')
    out=soup.find('a', class_='text-primary').text
    Stories['ScamType']=out

for Stories in data['Stories']:
    Stories['Description'] = Stories['Description'].replace('&hellip;...','...')
    Stories['Description'] = Stories['Description'].replace('â€™',"'")
#    Stories['Description'] = Stories['Description'].replace('. ','. \n')
#    Stories['Description'] = Stories['Description'].replace('! ','! \n')
#    Stories['Description'] = Stories['Description'].replace('? ','? \n')

with open('..\\new_debug.json','w') as f:
    json.dump(data, f, indent =2)


# For searching but not sure what t do with it
with open('..\\new_debug.json') as f:# file path of jason
    data = json.load(f)# input json file to data

search_text=input("Search by date (dd/mm/yyyy) or (mm) or (yyyy) > ")
output_date = str()
month_mapping={
    '01':'Jan',
    '02':'Feb',
    '03':'Mar',
    '04':'Apr',
    '05':'May',
    '06':'Jun',
    '07':'Jul',
    '08':'Aug',
    '09':'Sep',
    '10':'Oct',
    '11':'Nov',
    '12':'Dec',
}
if search_text.find('/')>=0:
    search_text = search_text.split('/')
    output_date=search_text[0]+' '+month_mapping.get(search_text[1])+' '+search_text[2]
elif len(search_text)==4:
    output_date = search_text
else:
    output_date=month_mapping.get(search_text)

for Stories in data['Stories']:
    if Stories['Date'].find(output_date) >= 0:
        print('\n' + Stories['Date'] + ' (' + Stories['ScamType'] + ')' + '\n' + Stories['Title'] + '\n' + 'https://www.scamalert.sg/'+Stories['Url'])

