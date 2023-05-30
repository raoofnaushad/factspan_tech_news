
from bs4 import BeautifulSoup

from src.config import *
from src.utils import *


def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')

    posts = soup.find('div', class_='ui-list')
    articles = posts.find_all('li')

 
    for article in articles:
        link = OPENAI_LINK + '/' + article.a['href'].split('/')[-1]
        article_links.append(link)
    
    article_links = article_links[:3]            
    return article_links

def scrape_each_article(link):
    try:
        content = get_html_content(link)
        soup = BeautifulSoup(content, 'lxml')
        heading = soup.title.text

        article = soup.find('div', id='content')
        main_content = article.findAll(True, {'class':['ui-block ui-block--text', 'ui-block ui-block--heading']})
        article_content = '\n\n'.join(para.text for para in main_content)
        if len(main_content) == 0:
            print(f"Issue scraping the link: {link}")
            raise
        else:    
            content = {
                        "date" : today,
                        "article": heading,
                        "image": "",
                        "text": article_content,
                        "c2a_link": link,
                    }
            # print(f"Successfully scraped the link: {link}")
            return content

    except Exception as ex:
        print(f"Some error with the link: {link}")
        print(f"Error: {str(ex)}")
        print(f"***"*5)
        return None




def main():
    contents = list()
    content = get_html_content(OPENAI_LINK)
    articles = get_article_links(content)

    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)

    # print(f"Number of articles from TOI: {len(contents)}")
    return contents
