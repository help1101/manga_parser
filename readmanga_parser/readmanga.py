import json
import requests
from bs4 import BeautifulSoup


class ReadManga:
    URL = 'https://readmanga.io'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    def request(self, link='', params=None):
        html = requests.get(self.URL + link, headers=self.HEADERS, params=params)
        return html

    def get_content(self, link='', params=None):
        html = self.request(link, params)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup

    def get_popular(self):
        items = self.get_content().select('.rightBlock .mangaList li .manga-link')
        response = []
        print(self.get_content())
        for i in items:
            if i.get_text():
                author = i.get('title').split(':')[0]
                genres = i.get('title').split(':')[-1]
                data = {"title": i.get_text(),
                        "author": author if author != genres else '',
                        "genres": genres,
                        "manga_url": i.get('href'),
                        "picture_url": ""
                        }

                response.append(data)
            else:
                data.update({"picture_url": i.get('rel')})

        result = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/popular.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def get_manga(self, manga_url):
        items = self.get_content(manga_url)
        manga_info = items.select('.leftContent')
        manga_chapters = items.select('.table-hover tr')
        chapters = []

        for i in manga_info:
            pictures = i.find('div', {'class': 'subject-cover'}).find_all('img')

            # sometimes titles can be without original title name
            try:
                original_title = i.find('h1', {'class': 'names'}).find_all('span')[2].get_text()
            except IndexError:
                original_title = ''

            left_content = {
                "ru_title": i.find('h1', {'class': 'names'}).find_all('span')[0].get_text(),
                "en_title": i.find('h1', {'class': 'names'}).find_all('span')[1].get_text(),
                "original_title": original_title,

                "rating": i.find('div', {'class': 'col-sm-7'}).find('span', {'class': 'rating-block'}).get(
                    'data-score'),

                "volumes_and_status": " ".join(
                    i.find('div', {'class': 'col-sm-7'}).find('div', {'class': 'subject-meta'}).find(
                        'p').get_text().split()),

                "genres": " ".join(
                    i.find('div', {'class': 'col-sm-7'}).find('p', {'class': 'elementList'}).get_text().split()),

                "year": i.find('div', {'class': 'col-sm-7'}).find('span', {'class': 'elem_year'}).get_text(),

                "description": " ".join(i.find('div', {'class': 'manga-description'}).get_text().split()),

                "pictures_url": [x.get('src') for x in pictures],

                "chapters": ""
            }

        for u in manga_chapters:
            chapter_date = u.find('td', {'class': 'd-none'}).get('data-date')

            chapter_info = {
                "chapter": " ".join(u.find('td', {'class': 'item-title'}).get_text().split()),
                "date": "",
                "href": u.find('a').get('href')
            }

            if chapter_date:
                chapter_info.update({"date": chapter_date})
            else:
                chapter_info.update({"date": " ".join(u.find_all('td', {'class': 'd-none'})[1].get_text().split())})

            chapters.append(chapter_info)

            left_content.update({"chapters": chapters})

        result = json.dumps(left_content, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/manga_data.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def reader(self, manga_url):
        from .manga_magic import main

        items = self.get_content(manga_url)
        manga_slides = items.select('.reader-controller')

        for i in manga_slides:
            script = str(i.find('script', type="text/javascript"))

        script_array = script.split()
        manga_pages = main(script_array)
        next_chapter_url = script_array[13].replace('"', '').replace(';', '')

        manga_reader = {
            "next_chapter_url": next_chapter_url,
            "manga_pages": manga_pages
        }
        result = json.dumps(manga_reader, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/manga_reader.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def search(self, query=''):
        items = self.request(link='/search/suggestion', params={'query': query}).json()

        result = json.dumps(items, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/manga_search.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result
