import requests
from bs4 import BeautifulSoup

# ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "upgrade-insecure-requests": "1"}

# header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'}
# req = requests.get("https://en.wikipedia.org/wiki/List_of_Tom_Hanks_performances", headers=headers)
req = requests.get("https://en.wikipedia.org/wiki/Robert_Downey_Jr._filmography", headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')
# print(soup.prettify())

index = open("index.html", "w", encoding='utf-8')
index.write(soup.prettify())
index.close()


csv = open("csv/tomHanksWiki.csv", "w", encoding='utf-8')

table = soup.find('table', class_='wikitable sortable plainrowheaders')

if table == None:
    table = soup.find('table', class_='wikitable plainrowheaders sortable')

rows = table.find_all('tr')

tableHead = table.find_all('th', attrs={'scope': 'col'})
print(tableHead)

if len(tableHead) > 5:
    year = tableHead[0].get_text().rstrip()
    title = tableHead[1].get_text().rstrip()
    actor = tableHead[5].get_text().rstrip()
    producer = tableHead[6].get_text().rstrip()
    role = tableHead[7].get_text().rstrip()
    csv.write(year + ',' + title + ',' + actor + ',' + producer + ',' + role + '\n')
else:
    year = tableHead[0].get_text().rstrip()
    title = tableHead[1].get_text().rstrip()
    role = tableHead[2].get_text().rstrip()
    csv.write(year + ',' + title + ',' + role + '\n')


# print(tableHead[0].get_text())

# tableHead = table.find_all('th', attrs={'scope': 'row'})

# https://iqss.github.io/dss-webscrape/web-scraping-approaches.html

body = table.find_all('tr')

year = 0

for i in range(2, len(body)):

    th = body[i].find('th', attrs={'scope':'row'})
    if(th != None):
        year = th.get_text().rstrip()

    cols = body[i].find_all('td')
    if len(tableHead) > 5:
        title = cols[0].get_text().rstrip()
        actor = cols[1].get_text().rstrip()
        producer = cols[2].get_text().rstrip()
        role = cols[3].get_text().rstrip()

        csv.write(year + ',' + title + ',' + actor + ',' + producer + ',' + role + '\n')
    else:
        title = cols[0].get_text().rstrip()
        role = cols[1].get_text().rstrip()

        csv.write(year + ',' + title + ',' + role + '\n')


csv.close()









