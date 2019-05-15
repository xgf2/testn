import db, save
from jinja2 import Environment, PackageLoader, select_autoescape

def news_from_db():

    list_news = db.get_amount_rows('list_news', '10')
    news = db.get_all_rows('news')

    env = Environment(
        loader=PackageLoader('view', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('list_news.html')

    return template.render(list_news=list_news, news = news, static_css = '/css/style.css')


def news_from_site():

    db.delete_all_rows('list_news')
    db.delete_all_rows('news')
    save.save_news_from_site_to_db()

    return news_from_db()

if __name__ == '__main__':
    print(news_from_site())

