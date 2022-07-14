import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup


class ReadManga():
    URL = 'https://readmanga.io'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    def request(self, link='', params=None):
        if self.URL in link:
            html = requests.get(link, headers=self.HEADERS, params=params)
            return html
        else:
            html = requests.get(self.URL + link, headers=self.HEADERS, params=params)
            return html

    def get_content(self, link='', params=None):
        html = self.request(link, params)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup

    def get_popular_now(self):
        items = self.get_content().select('.rightBlock .mangaList li .manga-link')
        response = []

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

        final_data = {"popular": response}

        result = json.dumps(final_data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/popular.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def get_manga(self, manga_url):
        print(f'getting {manga_url}')
        items = self.get_content(manga_url)
        manga_info = items.select('.leftContent')
        manga_chapters = items.select('.table-hover tr')
        chapters = []

        manga_data = {
            "catalogue": {
                "language": {
                    "ru": {
                        "readmanga": {
                            "manga_info": {

                            }
                        }
                    }
                }
            }
        }

        for i in manga_info:
            titles = i.find('h1', {'class': 'names'}).find_all('span')
            status = " ".join(
                i.find('div', {'class': 'col-sm-7'}).find('div', {'class': 'subject-meta'}).find(
                    'p').get_text().split())

            try:
                titles_list = [x.get_text() for x in titles]
            except IndexError:
                pass

            left_content = {
                "titles": titles_list,

                "rating": f"{i.find('div', {'class': 'col-sm-7'}).find('span', {'class': 'rating-block'}).get('data-score')}/5",

                "img": i.find('div', {'class': 'subject-cover'}).find('img').get('src'),

                "genres": i.find('div', {'class': 'col-sm-7'}).find('p', {'class': 'elementList'}).get_text().replace(
                    ',', '').split(),

                "year": int(i.find('div', {'class': 'col-sm-7'}).find('span', {'class': 'elem_year'}).get_text()),

                "manga_сompleted": True if 'завершено' in status else False,

                "description": " ".join(i.find('div', {'class': 'manga-description'}).get_text().split()),

                "chapters": {}
            }

        for u in manga_chapters:
            chapter_date = u.find('td', {'class': 'd-none'}).get('data-date')
            chapter_url = self.URL + u.find('a').get('href')

            chapter_info = {
                "chapter_name": " ".join(u.find('td', {'class': 'item-title'}).get_text().split()),
                "chapter_url": chapter_url,
                "release_date": "",
                "images_urls": self.reader(chapter_url),
            }

            if chapter_date:
                chapter_info.update({"date": chapter_date})
            else:
                chapter_info.update({"date": " ".join(u.find_all('td', {'class': 'd-none'})[1].get_text().split())})

            chapters.append(chapter_info)

            left_content.update({"chapters": chapters})

        result = json.dumps(left_content, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/manga_data.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def reader(self, chapter_url):
        from .manga_magic import main

        items = self.get_content(chapter_url)
        manga_slides = items.select('.reader-controller')

        for i in manga_slides:
            script = str(i.find('script', type="text/javascript"))

        # TODO: implement try except when no chapters
        # TODO: fix problem with https://readmanga.io/elektrosens
        # manga_slides = items.select('reader-controller')

        script_array = script.split()
        result = main(script_array)

        return result

    def search(self, query=''):
        items = self.request(link='/search/suggestion', params={'query': query}).json()

        result = json.dumps(items, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

        with open('readmanga_parser/manga_search.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result

    def get_popular(self, offset=0):
        """
        :param offset: this number equals quantity of titles on the page. 70 titles per page. range: [0 : 23660],
        step=70
        :return:
        """
        # https://readmanga.io/list?sortType=RATING&offset=
        # offset [0, 23660], 70 titles per page
        items = self.get_content(f'https://readmanga.io/list?sortType=RATING&offset={offset}').select(
            '.tile.col-md-6')
        title_counter = 0
        data_list = []

        for i in items:
            href = i.find('a', {'class': 'non-hover'}).get('href')
            data = {
                'href': href,
                'title': i.find('a', {'class': 'non-hover'}).find('img').get('title'),
                'picture_url': i.find('a', {'class': 'non-hover'}).find('img').get('data-original')
            }
            data_list.append(data)

            # getting data from each title

            self.get_manga(href)

            title_counter += 1

        if offset <= 70:
            if title_counter == 70:
                self.get_popular(offset + title_counter)

    #
    # def get_popular_now(self):
    #     items = self.get_content().select('.rightBlock .mangaList li .manga-link')
    #     response = []
    #
    #     for i in items:
    #         if i.get_text():
    #             author = i.get('title').split(':')[0]
    #             genres = i.get('title').split(':')[-1]
    #             data = {"title": i.get_text(),
    #                     "author": author if author != genres else '',
    #                     "genres": genres,
    #                     "manga_url": i.get('href'),
    #                     "picture_url": ""
    #                     }
    #
    #             response.append(data)
    #         else:
    #             data.update({"picture_url": i.get('rel')})
    #
    #     final_data = {"popular": response}
    #
    #     result = json.dumps(final_data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
    #
    #     with open('readmanga_parser/popular.json', 'w', encoding='utf-8') as file:
    #         file.write(result)
    #     return result


if __name__ == 'main':
    q = ReadManga()
    # q.get_popular()
    q.get_popular()

    # 'https://readmanga.io/podniatie_urovnia_v_odinochku__A56ff'
