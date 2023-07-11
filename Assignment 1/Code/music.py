import requests
from bs4 import BeautifulSoup
import re

HEADERS = ({'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'})

url = 'https://en.wikipedia.org/wiki/Category:Drake_(musician)_songs'

header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47'}

req = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(req.content, 'html.parser')
# print(soup.prettify())

songs = soup.find('div', class_='mw-category mw-category-columns')
# print(songs)

f = open("csv/wikipedia.csv", "w")
f.write("Title,WikipediaLink\n")

links = songs.find_all('a', href=True)
for link in links:

    title = link.get_text()
    # print(link.get_text())
    linkUrl = 'https://wikipedia.org' + link.get('href')
    print(linkUrl)
    f.write(title + ',' + linkUrl + '\n')

    # linkReq = requests.get(linkUrl, headers=HEADERS)
    # linkSoup = BeautifulSoup(linkReq.content, 'html.parser')

    youtubeSearch = title.replace(' ', '+')

    youtubeUrl = 'https://www.youtube.com/results?search_query=' + youtubeSearch
    print(youtubeUrl)

    youtubeReq = requests.get(youtubeUrl, headers=HEADERS)
    youtubeSoup = BeautifulSoup(youtubeReq.content, 'html.parser')
    print(youtubeSoup.prettify())

    # videos = youtubeSoup.find_all('a', id="video-title")

    # print(videos)
    break

    # data = linkSoup.find_all('th', class_ = re.compile('^infobox'))
    # dateLabel = linkSoup.find('th', class_='infobox-label').get_text()
    # print(dateLabel)
    # if dateLabel == 'Released':
    #     record = linkSoup.find('td', class_='infobox-data plainlist')
    #     print(record.get_text())
    # elif dateLabel == 'Recorded':
    #     release = linkSoup.find('td', class_='infobox-data published')
    #     print(release.get_text())


    # print(release)
    # print(record)

    # print(data.get_text())

    # id, title, artist, released, length

    # linkReq = requests.get(linkUrl, headers=HEADERS)
    # linkSoup = BeautifulSoup(linkReq.content, 'html.parser')
    # print(linkSoup.prettify())
    # break



# print(test)

# info = soup.find_all('h3', {'class': 'manga_h3'})
#
# for input in info:
#     print(input.get_text())





