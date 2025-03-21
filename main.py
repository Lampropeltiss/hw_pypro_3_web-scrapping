import requests
import bs4


def get_soup(link):
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    return soup


def print_articles(articles):
    """Print any list of articles"""
    for article in articles:
        article_info = [article['date'], article['title'], article['link']]
        print('{:17} | {:80} | {:20}'.format(*article_info))


def get_article_info(article, link_head):
    """Get info (title, link, date) for article from article soup"""
    article_title = article.find(name='h2', class_=['tm-title', 'tm-title_h2']).text
    article_link = link_head + article.find('a', class_='tm-title__link')['href']
    # article_date = article.find(name='div', class_='tm-article-snippet__meta').find('time')['title']
    article_date = article.find('time')['title']

    article_info = {'title': article_title, 'link': article_link, 'date': article_date}
    return article_info


def filter_and_print_articles(filter_words, link, link_head):
    """Get and print info (date, title, link) for articles filtered with keywords in preview."""
    soup = get_soup(link)
    article_soup_list = soup.find_all(name='article', class_='tm-articles-list__item')
    articles = []
    for article in article_soup_list:
        preview_text = article.text
        for word in filter_words:
            if word in preview_text:
                article_info = get_article_info(article, link_head)
                # print(f'found {word} in {article_info['title']}')
                articles.append(article_info)
                break
    print_articles(articles)


def filter_full_articles(articles, filter_words):
    """Filter articles by having the filter words in text."""
    filtered_articles = []
    for article in articles:
        soup = get_soup(article['link'])
        text = soup.find(name='div', class_='article-formatted-body').find_all('p')

        counter = dict.fromkeys(filter_words, 0)
        for p in text:
            for word in filter_words:
                if word.lower() in str(p).lower():
                    counter[word] += 1
                    # print(f'found {word} in {title}')
        if sum(counter.values()) > 0:
            filtered_articles.append(article)
    return filtered_articles


def get_all_articles(link, link_head):
    """Get info (date, title, link) for all articles without filters."""
    soup = get_soup(link)
    article_soup_list = soup.find_all(name='article', class_='tm-articles-list__item')
    articles = []
    for article in article_soup_list:
        articles.append(get_article_info(article, link_head))
    return articles


def filter_and_print_articles_pro(filter_words, link, link_head):
    """Get and print info (date, title, link) for articles filtered with keywords in text."""
    all_articles = get_all_articles(link, link_head)
    # print_articles(all_articles)
    # print()
    filtered_articles = filter_full_articles(all_articles, filter_words)
    print_articles(filtered_articles)


if __name__ == '__main__':
    keywords_1 = ['дизайн', 'фото', 'web', 'python']
    keywords_2 = ['ChatGPT', 'Django', 'AI', 'IT', 'API']
    habr_link = 'https://habr.com/ru/articles/'
    habr_link_head = 'https://habr.com'

    print('Preview filter')
    filter_and_print_articles(keywords_1, habr_link, habr_link_head)
    print()
    print('Text filter')
    filter_and_print_articles_pro(keywords_1, habr_link, habr_link_head)
