import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse


def clear_html_text_from_tags(html):
    # return html
    return BeautifulSoup(html, "lxml").text


class MangaUtils:

    @staticmethod
    def parse_main_content_for_manga_page(main_content):
        title = main_content.select_one('span.releasestitle')
        panels = main_content.select('div.col-6.p-2.text')
        if len(panels) != 2:
            return
        left = MangaUtils.parse_manga_left_panel(panels[0])
        right = MangaUtils.parse_manga_right_panel(panels[1])
        result = {**left, **right}
        result['title'] = title.string
        return result

    @staticmethod
    def process_panel_items(content, handlers):
        result = {}

        def extract_section_header(ct):
            result = ct.previous_sibling.previous_sibling.select_one("b").string
            return result if result is not None else clear_html_text_from_tags(
                ct.previous_sibling.previous_sibling.encode_contents())

        for section in content:
            header = extract_section_header(section)
            if header in handlers:
                result[handlers[header]["name"]] = handlers[header]["func"](section)
        return result

    @staticmethod
    def extract_description_from_div(description_div):
        extended_description = description_div.select_one('#div_desc_more')
        if extended_description:
            return clear_html_text_from_tags(extended_description.encode_contents()).strip()

        return clear_html_text_from_tags(description_div.encode_contents()).strip()

    @staticmethod
    def extract_type_from_div(type_div):
        return type_div.string.strip()

    @staticmethod
    def extract_associated_names_from_div(associated_names):
        names = associated_names.encode_contents()  # .split("<br>")

        def extract_single_alternative_name(br_tag):
            return br_tag.previous_sibling

        return [extract_single_alternative_name(br_tag) for br_tag in associated_names.select('br')]

    @staticmethod
    def extract_image_from_div(img_div):
        img = img_div.select_one('img')
        return img["src"]

    @staticmethod
    def extract_genres_from_div(genres_dev):
        def strip_search_link_from_the_end(ls):
            return ls[:-1]

        result = [genre.next_element.string for genre in genres_dev.select('a')]
        return strip_search_link_from_the_end(result)

    @staticmethod
    def extract_author_from_div(author_div):
        pass

    @staticmethod
    def parse_manga_left_panel(left):
        content = left.select('div.sCat + div.sContent')

        handlers = {
            'Description': {'func': MangaUtils.extract_description_from_div, 'name': 'description'},
            'Type': {'func': MangaUtils.extract_type_from_div, 'name': 'type'},
            "Associated Names": {'func': MangaUtils.extract_associated_names_from_div, 'name': 'names'},
            "Author": {}
        }

        return MangaUtils.process_panel_items(content, handlers)

    @staticmethod
    def parse_manga_right_panel(right):
        content = right.select('div.sCat + div.sContent')
        handlers = {
            'Image': {'func': MangaUtils.extract_image_from_div, 'name': 'img'}
            , 'Genre': {'func': MangaUtils.extract_genres_from_div, 'name': 'genres'}

        }
        return MangaUtils.process_panel_items(content, handlers)


class MangaUpdates:
    URL = 'https://www.mangaupdates.com'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    def get_full_url(self, link):
        parsed = urlparse(link)
        return self.URL + link if parsed.netloc == '' else link

    def request(self, link='', params=None):
        html = requests.get(self.URL + link, headers=self.HEADERS, params=params)
        return html

    def get_content(self, link='', params=None):
        html = self.request(link, params)
        if html.status_code == 200:
            print("OK")
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup

    def get_popular_nice(self):
        params = {
            'perpage': 100, 'orderby': 'rating', 'page': 1}
        items = self.get_content('/series.html', params=params).select('div.col-12.col-lg-6.p-3.text')
        # print( len(items))
        return [self.extract_single_popular_item(item) for item in items]

    def get_popular_nice_generator(self, first_page=1, last_page=1):
        page = first_page
        params = {'perpage': 100, 'orderby': 'rating', 'page': page}
        while page <= last_page:
            params["page"] = page
            items = self.get_content('/series.html', params=params).select('div.col-12.col-lg-6.p-3.text')
            if items is None:
                break
            for item in items:
                yield self.extract_single_popular_item(item)
            page = page + 1

    def extract_single_popular_item(self, item):
        imgTag = item.find('img')
        aTag = item.find('a')
        titleTag = item.select_one("u >b")
        return {
            "title": titleTag.encode_contents()
            , "is_adult": imgTag is not None
            , "img_src": imgTag['src'] if imgTag is not None else ""
            , 'link': aTag['href']
        }

    def get_manga_page_by_url(self, url):
        # url can be full url or relative
        parsedUrl = urlparse(url)
        # print(parsedUrl)
        # print(urlparse(self.URL))
        full_url = self.get_full_url(url)
        print(full_url)
        html = requests.get(full_url, headers=self.HEADERS)
        if html.status_code != 200:
            return
            # print("OK")
        soup = BeautifulSoup(html.text, 'html.parser')
        if soup is None:
            return

        main_content = soup.select_one('#main_content')
        return MangaUtils.parse_main_content_for_manga_page(main_content)

    def get_popular(self):
        items = self.get_content('/series.html?perpage=100&orderby=rating').select('#main_content')
        self.get_content().find_parent()

        response = []

        for i in items:
            title = i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find_parent('div', {
                'class': 'col-12 col-lg-6 p-3 text'.split()}).find('div', {'class': 'text'}).find('a').text
            genres = i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find_parent('div',
                                                                                                                 {
                                                                                                                     'class': 'col-12 col-lg-6 p-3 text'.split()}).find(
                'div', {'class': 'textsmall'}).find('a').text
            data = {
                'title': i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find_parent(
                    'div', {'class': 'col-12 col-lg-6 p-3 text'.split()}).find('div', {'class': 'text'}).find('a').text,
                'genres': i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find_parent(
                    'div', {'class': 'col-12 col-lg-6 p-3 text'.split()}).find('div', {'class': 'textsmall'}).find(
                    'a').get('title'),
                'description': ' '.join(" ".join(
                    i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find_parent('div', {
                        'class': 'col-12 col-lg-6 p-3 text'.split()}).find('div', {
                        'class': 'text flex-grow- 1'.split()}).text.split()).replace(title, '').replace(genres,
                                                                                                        '').split()),
                'year': '',
                'rating': '',
                'manga_page_url': i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find(
                    'a').get('href'),
                'picture_url': i.find('div', {'class': 'col-auto align-self-center series_thumb p-0'.split()}).find(
                    'img').get('src')
            }
            response.append(data)
        print(response)


q = MangaUpdates()
# popular = q.get_popular_nice()
# pprint(popular)
# popular = q.get_popular_nice_generator(first_page=1, last_page=4)
# for a in popular:
#     print(a)
# print(popular)

manga = q.get_manga_page_by_url('https://www.mangaupdates.com/series.html?id=70001')
manga2 = q.get_manga_page_by_url('/series.html?id=146700')

pprint(manga)
# print(manga2)
