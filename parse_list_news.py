import http.client as client
from lxml import etree
import re, settings
from datetime import date

def parse_list_news():
    try:
        # re.search('([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9])', 'https://rostov.rbc.ru/rostov/07/05/2019/5cd1969d9a7947ee34a48213').groups()
        # url central column: https://rostov.rbc.ru/v10/ajax/central-column/rostov/
        # url root: rostov.rbc.ru
        connection = client.HTTPSConnection(settings.HOST_URL)
        connection.request('GET', settings.HOST_PATH)
        response = connection.getresponse()

        if response.status == 200:
            html_data = response.read()
            connection.close()

            tree = etree.fromstring(html_data, etree.HTMLParser())

            list_crude_news = tree.cssselect('a.item__link') #item__link') #main__feed__link')div.js-index-central-column-big 

            list_news = []
            for news in list_crude_news:
                href = news.attrib.get('href')

                crude_title = news.cssselect('span.item__title')  #main__feed__title')
                title = crude_title[0].text
                title = title.replace('\n', '')
                title = title.strip()

                crude_image_src= news.cssselect('img.item__image') #main__feed__title')
                if len(crude_image_src) != 0:
                    image_src = crude_image_src[0].get('src')
                else:
                    image_src = None

                crude_date_news = re.search('([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9])', href)
                if crude_date_news is None:
                    date_news = date.today()
                else:
                    date_news_tuple = crude_date_news.groups()
                    date_news = date(int(date_news_tuple[2]), int(date_news_tuple[1]), int(date_news_tuple[0])) 

                list_news.append({'href': href, 'title': title, 'image_src': image_src, 'date_news': date_news})

            return (list_news)

        else:
            print(response.status)

    except ValueError as message_error:
        print(message_error)


if __name__ == '__main__':
    print(parse_list_news())
