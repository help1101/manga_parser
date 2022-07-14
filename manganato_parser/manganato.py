import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class MangaKakalot:
    URL = 'https://manganato.com'
    READER_URL = 'https://readmanganato.com'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    def request(self, link='', prefix='', params=None):
        html = requests.get(prefix+self.URL + link, headers=self.HEADERS, params=params)
        return html

    def get_content(self, link='', params=None):
        html = self.request(link, params)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup

    def get_popular(self, page_number=1):
        items = self.get_content(f'/genre-all/{page_number}?type=topview')
        response = []

        cards = items.find_all('div', {'class': 'content-genres-item'})
        for i in cards:

            data = {
                'title': i.find('h3').text,
                'author': i.find('span', {'class': 'genres-item-author'}).text,
                'rating': f'{i.find("em", {"class": "genres-item-rate"}).text}/5',
                'manga_url': i.find('a', {'class': 'genres-item-img'}).get('href'),
                'picture_url': i.find('img', {'class': 'img-loading'}).get('src'),
                'description': " ".join(i.find('div', {'class': 'genres-item-description'}).text.split()),
            }
            response.append(data)
        result = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('popular.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def get_manga(self, manga_url):
        # url = https://readmanganato.com/manga-dr980474
        items = self.get_content(manga_url)
        print(items)
        manga_info = items.select('.container-main-left')
        print(manga_info)


        # for i in manga_info:
        #     print(i)
        #     data = {
        #         'title': '',
        #         'author': '',
        #         'status': '',
        #         'genres': '',
        #         'rating': '',
        #         'chapters': {
        #             'chapter': '',
        #             'chapter_date': '',
        #             'chapter_url': ''
        #         }
        #     }






    def get_reader(self, chapter_url):
        pass

    def search(self, queue):
        pass


if __name__ == '__main__':
    q = MangaKakalot()
    # q.get_popular(1)

    q.get_manga('/manga-dr980474')
