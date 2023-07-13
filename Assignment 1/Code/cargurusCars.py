import requests
from bs4 import BeautifulSoup

# ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "upgrade-insecure-requests": "1"}

# header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'}
# req = requests.get("https://en.wikipedia.org/wiki/List_of_Tom_Hanks_performances", headers=headers)
# https://milwaukee.craigslist.org/search/sss?query=car#search=1~gallery~0~


def scrapeCraigslist(websites):
    csv = open("csv/cargurusCars.csv", "w", encoding='utf-8')
    csv.write('ID,Title,Price,Miles,Location,Market Price\n')
    id = 1

    for website in websites:
        req = requests.get(website, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        # print(soup.prettify())

        # index = open("cargurusCars.html", "w", encoding='utf-8')
        # index.write(soup.prettify())
        # index.close()

        carTitle = []
        for title in soup.find_all('h4', class_='titleText'):
            carTitle.append(title.get_text().strip())
        # print(carTitle)

        carPrice = []
        for price in soup.find_all('span', class_='price'):
            price = price.find('span').get_text().strip()
            carPrice.append(price.replace(',', ''))
        # print(carPrice)

        carMiles = []
        for mileage in soup.find_all('p', class_='mileageText'):
            mileage = mileage.find_all('span')[-1].get_text().strip()
            carMiles.append(mileage.replace(',', ''))
        # print(carMiles)


        carLocation = []
        for location in soup.find_all('p', class_='distanceAndLocationText'):
            if location is not None:
                location = location.find_all('span')[-1].get_text()
                location = location.split('(')[0].strip()
                # location = location.replace(',', ';')
                carLocation.append('\"' + location + '\"')
            else:
                carLocation.append('unknown')

        carMarket = []
        for market in soup.find_all('div', class_='dealRatingDescription'):
             carMarket.append(market.get_text().strip().replace(',', ''))



        # for details in soup.find_all('div', class_='details'):
        #     price = details.find('div', class_='price')
        #     carPrice.append(price.get_text().strip())
        #
        #     location = details.find('div', class_='location')
        #

        assert(len(carTitle) == len(carPrice) == len(carMiles) == len(carLocation) == len(carMarket))

        for i in range(0, len(carPrice)):
            csv.write(str(id) + ',')
            csv.write(carTitle[i] + ',')
            csv.write(carPrice[i] + ',')
            csv.write(carMiles[i] + ',')
            csv.write(carLocation[i] + ',')
            csv.write(carMarket[i] + '\n')
            id += 1
        print(id)
    csv.close()



if __name__ == '__main__':

    websites = []
    site = 'https://www.cargurus.com/Cars/spt_used_cars-Brookfield_L39536#resultsPage={}'

    # for i in range(1, 1523):
    for i in range(1, 100):
        websites.append(site.format(i))

    # carGuru = ['https://www.cargurus.com/Cars/spt_used_cars-Brookfield_L39536#resultsPage=1']
    # tampaCraigslist = 'https://tampa.craigslist.org/search/sss?query=car#search=1~gallery~0~0'
    # dallasCraigslist = 'https://dallas.craigslist.org/search/sss?query=car#search=1~gallery~0~0'

    # websites = [mkeCraigslist, tampaCraigslist, dallasCraigslist]

    scrapeCraigslist(websites)
    print('Success')



