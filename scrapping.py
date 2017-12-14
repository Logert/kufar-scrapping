from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def getNews():
    result = []
    for page in range(1, 100):
        url = 'https://www.kufar.by/%D0%B1%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C/%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D1%8B/macbook?&o=' + str(page)
        news = getUrl(url)
        if (len(news) != 0):
            for item in news:
                info = item.find('div', {'class': 'list_ads__info_container'})

                title = info.find('a', {'class': 'list_ads__title'}).getText()
                link = info.find('a', {'class': 'list_ads__title'}).get('href')
                price = info.find('b', {'class': 'list_ads__price'}).span
                time = info.find('time', {'class': 'list_ads__date'}).get('datetime')
                images = item.find('div', class_='list_ads__image_container').find('a').get('data-images')
                listImages = []
                if (len(images) != 0):
                    for image in images.split(','):
                        listImages.append('https://content.kufar.by/line_thumbs' + image)
                if (price != None):
                    price = float(price.getText().split(' р.')[0].replace(',', '.').replace(' ', ''))
                else:
                    price = 0
                result.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "time": time,
                    "images": listImages
                })
        else:
            break
    return result


def getUrl(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0')
        html = urlopen(req)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.find_all('article', {'class': 'list_ads__item '})
    except AttributeError as e:
        return None
    return title


if __name__ == '__main__':
    text = getNews()
    print(text)
