import http.client as client
from lxml import etree
import re, settings
from datetime import datetime

def parse_news(href):
    try:
        # re.search('(https?://[a-z,.]*/' + th+')'+'(/[a-z,0-9,/,.]*)', 'https://rostov.rbc.ru/rostov/freenews/5cd049d29a79477b8349611c').groups()
        # re.search('([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9])', 'https://rostov.rbc.ru/rostov/07/05/2019/5cd1969d9a7947ee34a48213').groups()
        # url root: rostov.rbc.ru
        host_url = re.search(settings.HOST_URL, href).group()
        host_path = re.search('(' + settings.HOST_PATH + ')/([a-z,0-9,/,.]*)', href).group()

        connection = client.HTTPSConnection(host_url)
        connection.request('GET', host_path)
        response = connection.getresponse()

        if response.status == 200:
            html_data = response.read()
            connection.close()

            tree = etree.fromstring(html_data, etree.HTMLParser())

            title_news = tree.cssselect('span.js-slide-title')[0].text
            title_news = title_news.strip()

            image_news_src = tree.cssselect('img.article__main-image__image')
            if len(image_news_src) != 0:
                image_news_src = image_news_src[0].attrib.get('src')
            else:
                image_news_src = None

            crude_text_news = tree.cssselect('div.article__text > p')
            text_news = ''
            for news in crude_text_news:
                elem_news = etree.tostring(news, encoding = 'UTF-8', method = 'text').decode('utf-8')
                elem_news = elem_news.replace('\n', '')
                elem_news = elem_news.replace('\r', '')
                elem_news = elem_news.strip()
                text_news += elem_news
                text_news += ' '

            elems_date_news = tree.cssselect('span.article__header__date')

            if len(elems_date_news) != 0:
                crude_date_news = elems_date_news[0].attrib
                crude_date_news = crude_date_news.get('content')
                crude_date_news = crude_date_news.split('+')
                crude_date_news[1] = crude_date_news[1].replace(':','')
                crude_date_news = crude_date_news[0] + '+' + crude_date_news[1]
                date_news = datetime.strptime(crude_date_news, '%Y-%m-%dT%H:%M:%S%z')

            return {'href': href, 'title_news': title_news, 'image_src_news': image_news_src, 'text_news':  text_news, 'datetime_news': date_news}

        else:
            print(response.status)

    except ValueError as message_error:
        print(message_error)


if __name__ == '__main__':
    #print(parse_news('https://rostov.rbc.ru/rostov/freenews/5cd049d29a79477b8349611c'))
    print(parse_news('https://rostov.rbc.ru/rostov/08/05/2019/5cd2d7a09a79475ae3cdd0b5'))
