from pprint import pprint

from readmanga_parser.readmanga import ReadManga
from desu.parser import Desu
import time


start_time = time.monotonic()
q = Desu()
w = ReadManga()
# test = q.get_manga('https://desu.me/manga/x-tokyo-ghoul-re.185/')
# q.get_manga('https://desu.me/manga/my-daughters-s-rank-adventurers-have-a-severe-obsession.2813/')
# q.get_manga('https://desu.me/manga/the-newbie-is-too-strong.3659/')
# q.get_manga('https://desu.me/manga/z-arifureta-shokugyou-de-sekai-saikyou.851/')
# print(test)


q.get_popular()

print(f'Прошло: {time.monotonic() - start_time} сек')

