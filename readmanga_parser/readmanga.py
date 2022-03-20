import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class ReadManga:
    URL = 'https://readmanga.io'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    def get_content(self, link=''):
        html = requests.get(self.URL + link, headers=self.HEADERS)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup

    def get_list_of_popular_titles(self):
        response = []
        items = self.get_content().select('.rightBlock .mangaList li .manga-link')

        for i in items:
            if i.get_text():
                data = {"title": i.get_text(),
                        "author": i.get('title').split(':')[0],
                        "genres": i.get('title').split(': ')[-1],
                        "manga_url": i.get('href'),
                        "picture_url": ""
                        }

                response.append(data)
            else:
                data.update({"picture_url": i.get('rel')})

        with open('popular.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
        return json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

    def get_manga(self, manga_url):
        items = self.get_content(manga_url)
        manga_info = items.select('.leftContent')
        manga_chapters = items.select('.table-hover tr')
        chapters = []
        for i in manga_info:
            pictures = i.find('div', {'class': 'subject-cover'}).find_all('img')

            left_content = {
                "title_ru": i.find('h1', {'class': 'names'}).find_all('span')[0].get_text(),
                "title_en": i.find('h1', {'class': 'names'}).find_all('span')[1].get_text(),
                "title_jp": i.find('h1', {'class': 'names'}).find_all('span')[2].get_text(),

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

        # pprint(left_content)

        with open('manga_data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(left_content, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
        return json.dumps(left_content, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)






q = ReadManga()
q.get_manga('/dosanko_giaru_chudo_kak_mily__A5238')
