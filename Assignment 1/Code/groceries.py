import requests
from bs4 import BeautifulSoup

# products = ['chips', 'cereal', 'milk', 'crackers', 'soup', 'ice+cream', 'cookies']
products = ['chips']

# https://iqss.github.io/dss-webscrape/web-scraping-approaches.html

def getTargetData(targetUrl):


    for product in products:

        index = 0
        max = float('inf')

        while(index < max):
            targetUrl = 'https://target.com/s?searchTerm={}&Nao={}&moveTo=product-list-grid'.format(product, index)
            print(targetUrl)
            response = requests.get(targetUrl)
            soup = BeautifulSoup(response.content, "html.parser")
            count = soup.find('h2', attrs={'data-test': 'resultsHeading'})
            print(soup.prettify())
            print(count)
            break
            index += 24




    # product_title = soup.find("span", attrs={"id": "productTitle"})
    # print(product_title)
    # product_price = soup.find("span", attrs={"id": "priceblock_ourprice"}).get_text()
    # product_rating = soup.find("span", attrs={"id": "acrCustomerReviewText"}).get_text()

    return {
        # "product_title": product_title,
        # "product_price": product_price,
        # "product_rating": product_rating
    }


if __name__ == "__main__":
    targetUrl = 'https://www.target.com/'
    targetFile = 'PycharmProjects/CS 767/csv/target.csv'
    getTargetData(targetUrl)



    # walmartUrl = 'https://www.walmart.com/'
    # targetFile = 'PycharmProjects/CS 767/csv/walmart.csv'
    # getWalmartData(walmartUrl)
