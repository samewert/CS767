import requests
from bs4 import BeautifulSoup

# ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "upgrade-insecure-requests": "1"}

# header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'}
req = requests.get("https://www.iseecars.com/cars-for-sale#autoZip=False&Location=53045&Radius=50&_t=a&offset=100&maxResults=100&sort=BestDeal&sortOrder=desc&lfc_t0=MTY5MDA0MzIyMDc1Nw%3D%3D", headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify())
test = soup.find_all('a')
print(test)

index = open("scrapy.html", "w", encoding='utf-8')
index.write(soup.prettify())
index.close()

# info = soup.find_all('h3', {'class': 'manga_h3'})
#
# for input in info:
#     print(input.get_text())





