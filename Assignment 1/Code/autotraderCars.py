import requests
from bs4 import BeautifulSoup

# ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9", "upgrade-insecure-requests": "1"}

# header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'}
# req = requests.get("https://en.wikipedia.org/wiki/List_of_Tom_Hanks_performances", headers=headers)
# https://milwaukee.craigslist.org/search/sss?query=car#search=1~gallery~0~


def scrapeCraigslist(websites):
    csv = open("csv/autotraderCars.csv", "w", encoding='utf-8')
    csv.write('ID,Title,Price,Miles\n')
    id = 1

    for website in websites:
        req = requests.get(website, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        # print(soup.prettify())

        # index = open("autotraderCars.html", "w", encoding='utf-8')
        # index.write(soup.prettify())
        # index.close()

        carTitles = []

        for title in soup.find_all('h3', class_='text-bold text-size-300 link-unstyled'):
            title = title.get_text()

            if 'Used' in title:
                title = title.replace('Used ', '')
            elif 'Certified' in title:
                title = title.replace('Certified ', '')
            carTitles.append(title)

        carMiles = []
        for miles in soup.find_all('div', class_='item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter'):
            miles = miles.find('span')
            miles = miles.get_text().split(' ')[0]

            carMiles.append(miles.replace(',', ''))


        carPrice = []

        first = True
        for price in soup.find_all('span', class_='first-price'):
            if first:
                first = False
                continue
            price = price.get_text()
            carPrice.append(price.strip().replace(',',''))

        # carLocation = []
        #
        # for location in soup.find_all('div', class_='result-date-location'):
        #     location = location.find_all('span')
        #
        #     location = location[-1].get_text()
        #
        #     if '(' in location:
        #         location = location.split('(')[0]
        #     else:
        #         location = location.split('-')[0]
        #
        #     carLocation.append('\"' + location.strip() + '\"')

        for i in range(0, len(carPrice)):
            csv.write('b' + str(id) + ',')
            csv.write(carTitles[i] + ',')
            csv.write(carPrice[i] + ',')
            csv.write(carMiles[i] + '\n')
            # csv.write(carLocation[i] + '\n')
            id += 1
        print(id)


    csv.close()



if __name__ == '__main__':

    # mkeCraigslist = 'https://milwaukee.craigslist.org/search/sss?query=car#search=1~gallery~0~'
    # tampaCraigslist = 'https://tampa.craigslist.org/search/sss?query=car#search=1~gallery~0~0'
    # dallasCraigslist = 'https://dallas.craigslist.org/search/sss?query=car#search=1~gallery~0~0'

    # https://www.autotrader.com/cars-for-sale/brookfield-wi?isNewSearch=false&marketExtension=include&numRecords=24&searchRadius=50&showAccelerateBanner=false&sortBy=relevance&zip=53045
    # https://www.autotrader.com/cars-for-sale/brookfield-wi?firstRecord=24&isNewSearch=false&marketExtension=include&numRecords=24&searchRadius=50&showAccelerateBanner=false&sortBy=relevance&zip=53045
    # https://www.autotrader.com/cars-for-sale/brookfield-wi?firstRecord=48&isNewSearch=false&marketExtension=include&numRecords=24&searchRadius=50&showAccelerateBanner=false&sortBy=relevance&zip=53045
    # https://www.autotrader.com/cars-for-sale/brookfield-wi?isNewSearch=false&marketExtension=include&numRecords=100&searchRadius=50&showAccelerateBanner=false&sortBy=relevance&zip=53045
    cars = "https://www.autotrader.com/cars-for-sale/brookfield-wi?firstRecord={}&isNewSearch=false&marketExtension=include&numRecords=100&searchRadius=500&showAccelerateBanner=false&sortBy=relevance&zip=53045"

    websites = []

    for i in range(0, 1000, 100):
        websites.append(cars.format(i))

    cars = "https://www.autotrader.com/cars-for-sale/miami-fl?firstRecord={}&isNewSearch=false&marketExtension=include&numRecords=100&searchRadius=500&showAccelerateBanner=false&sortBy=relevance&zip=33101"
    for i in range(0, 700, 100):
        websites.append(cars.format(i))


    # https://www.iseecars.com/cars-for-sale#autoZip=False&Location=53045&Radius=50&_t=a&maxResults=20&sort=BestDeal&sortOrder=desc&lfc_t0=MTY5MDA0MzIyMDc1Nw%3D%3D
    # https://www.iseecars.com/cars-for-sale#autoZip=False&Location=53045&Radius=50&_t=a&offset=20&maxResults=20&sort=BestDeal&sortOrder=desc&lfc_t0=MTY5MDA0MzIyMDc1Nw%3D%3D
    # https://www.iseecars.com/cars-for-sale#autoZip=False&Location=53045&Radius=50&_t=a&offset=40&maxResults=20&sort=BestDeal&sortOrder=desc&lfc_t0=MTY5MDA0MzIyMDc1Nw%3D%3D



    scrapeCraigslist(websites)
    print('Success')




