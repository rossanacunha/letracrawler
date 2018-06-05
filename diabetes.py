import requests
from bs4 import BeautifulSoup

start_url = 'https://pt.wikipedia.org/wiki/Diabetes_mellitus'
domain = 'https://pt.wikipedia.org'


def get_soup(url):
    content = requests.get(url).content

    return BeautifulSoup(content.decode('utf-8'), 'html.parser')


def clean_input(content):
    content = bytes(content, "UTF-8")
    content = content.decode("UTF-8")
    sentences = content.split('. ')
    return sentences


def extract_links(paragraphs):
    tags = []

    for paragraph in paragraphs:
        tags.extend(paragraph.findAll('a'))

    tags = [tag for tag in tags if 'title' in tag.attrs and 'href' in tag.attrs]

    links = [tag.get('href') for tag in tags]

    return links


def extract_content(url=start_url):
    content = []

    soup = get_soup(url)

    content_items = soup.find('div', {'id': 'mw-content-text'})
    [script.extract() for script in content_items.find_all('script')]
    [script.extract() for script in content_items.find_all('sup')]
    content_items = content_items.find_all('p')
    content_links = extract_links(content_items)

    for content_item in content_items:
        texts = clean_input(content_item.get_text())
        for text in texts:
            if not text.isspace():
                content.append(text + "\n")

    return content, content_links


def extract_text(url=start_url):
    sentences = []

    content, links = extract_content(url)
    sentences.extend(content)

    for link in links:
        print('Items : {}'.format(len(sentences)))
        content, links = extract_content(domain + link)
        sentences.extend(content)
        if len(links) > 5000:
            break

    return sentences


def main():
    items = extract_text(url=start_url)

    with open('data/output.txt', 'w') as f:
        f.writelines(items)
