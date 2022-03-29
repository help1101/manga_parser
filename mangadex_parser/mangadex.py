import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class MangadexReader:
    URL = 'https://mangadex.org'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'}

    def request(self, link='', params=None):
        html = requests.get(self.URL + link, headers=self.HEADERS, params=params)
        return html

    def get_content(self, link='', params=None):
        html = self.request(link, params)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup

    def get_popular(self):
        html = requests.get(
            'https://api.mangadex.org/manga?limit=32&offset=0&includes[]=cover_art&includes[]=author&includes[]=artist&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&order[followedCount]=desc',
            headers=self.HEADERS).json()

        result = json.dumps(html, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        with open('popular.json', 'w', encoding='utf-8') as file:
            file.write(result)
        return result


if __name__ == '__main__':
    w = MangadexReader()

    # w.get_popular()
    print(w.get_popular())
