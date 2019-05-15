import db
from parse import parse_list_news, parse_news

def save_news_from_site_to_db():

    list_news = parse_list_news()

    new_list_news = []
    for elem in list_news:
        if not db.get_row_on_column('list_news', 'href', elem.get('href')):
            new_list_news.append(elem)

    news = []
    for elem in new_list_news:
        if not db.get_row_on_column('news', 'href', elem.get('href')):
            news.append(parse_news(elem.get('href')))

    # Replace datetime in list_news
    for elem_ln in new_list_news:
        for elem_n in news:
            if elem_n.get('href') == elem_ln.get('href'):
                elem_ln['date_news'] = elem_n['datetime_news']

    db.add_rows('list_news', new_list_news)
    db.add_rows('news', news)



if __name__ == '__main__':
    save_news_from_site_to_db()
