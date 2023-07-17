import requests
from bs4 import BeautifulSoup

# ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "upgrade-insecure-requests": "1"}

# header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'}
# req = requests.get("https://en.wikipedia.org/wiki/List_of_Tom_Hanks_performances", headers=headers)
# https://milwaukee.craigslist.org/search/sss?query=car#search=1~gallery~0~


def scrapeCraigslist(websites):
    csv = open("csv/craigslistCars.csv", "w", encoding='utf-8')
    csv.write('ID,Title,Price,Location\n')
    id = 1

    for website in websites:
        req = requests.get(website, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        # print(soup.prettify())

        # index = open("craigslistCars.html", "w", encoding='utf-8')
        # index.write(soup.prettify())
        # index.close()

        carTitle = []

        for title in soup.find_all('div', class_='title'):
            carTitle.append(title.get_text().replace(',',''))

        carPrice = []
        carLocation = []

        for details in soup.find_all('div', class_='details'):
            price = details.find('div', class_='price')
            carPrice.append(price.get_text().strip().replace(',',''))

            location = details.find('div', class_='location')
            if location is not None:
                carLocation.append(location.get_text().strip().replace(',',''))
            else:
                carLocation.append('unknown')

        assert(len(carTitle) == len(carPrice) == len(carLocation))

        for i in range(0, len(carPrice)):
            csv.write(str(id) + ',')
            csv.write(carTitle[i] + ',')
            csv.write(carPrice[i] + ',')
            csv.write(carLocation[i] + '\n')
            id += 1

    csv.close()



if __name__ == '__main__':

    mkeCraigslist = 'https://milwaukee.craigslist.org/search/sss?query=car#search=1~gallery~0~'
    tampaCraigslist = 'https://tampa.craigslist.org/search/sss?query=car#search=1~gallery~0~0'
    dallasCraigslist = 'https://dallas.craigslist.org/search/sss?query=car#search=1~gallery~0~0'

    websites = [mkeCraigslist, tampaCraigslist, dallasCraigslist]

    scrapeCraigslist(websites)
    print('Success')




