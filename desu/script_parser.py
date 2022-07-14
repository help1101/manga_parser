# test_script = """<script type="text/javascript">
#                 $(document).ready(function() {
#                     Reader.init({
#                         mirror: 1,
#                         dir: "//img2.desu.me/manga/rus/tokyo_ghoul_re/vol16_ch179/",
#                         mangaUrl: "/manga/tokyo-ghoul-re.185/",
#                         images: [["tokyo_ghoul_re_vol16_ch179_p001.jpg", 912, 1300], ["tokyo_ghoul_re_vol16_ch179_p002.jpg", 904, 1300], ["tokyo_ghoul_re_vol16_ch179_p003.jpg", 906, 1300], ["tokyo_ghoul_re_vol16_ch179_p004.jpg", 904, 1300], ["tokyo_ghoul_re_vol16_ch179_p005.jpg", 904, 1300], ["tokyo_ghoul_re_vol16_ch179_p006.jpg", 903, 1300], ["tokyo_ghoul_re_vol16_ch179_p007.jpg", 891, 1300], ["tokyo_ghoul_re_vol16_ch179_p008.jpg", 891, 1300], ["tokyo_ghoul_re_vol16_ch179_p009.jpg", 890, 1300], ["tokyo_ghoul_re_vol16_ch179_p010.jpg", 900, 1300], ["tokyo_ghoul_re_vol16_ch179_p011.jpg", 896, 1300], ["tokyo_ghoul_re_vol16_ch179_p012.jpg", 1799, 1300], ["tokyo_ghoul_re_vol16_ch179_p013.jpg", 894, 1300], ["tokyo_ghoul_re_vol16_ch179_p014.jpg", 886, 1300], ["tokyo_ghoul_re_vol16_ch179_p015.jpg", 889, 1300], ["tokyo_ghoul_re_vol16_ch179_p016.jpg", 882, 1300], ["tokyo_ghoul_re_vol16_ch179_p017.jpg", 879, 1300], ["tokyo_ghoul_re_vol16_ch179_p018.jpg", 887, 1300], ["tokyo_ghoul_re_vol16_ch179_p019.jpg", 880, 1300], ["tokyo_ghoul_re_vol16_ch179_p020.jpg", 884, 1300], ["tokyo_ghoul_re_vol16_ch179_p021.jpg", 889, 1300], ["tokyo_ghoul_re_vol16_ch179_p022.jpg", 888, 1300], ["tokyo_ghoul_re_vol16_ch179_p023.jpg", 884, 1300], ["tokyo_ghoul_re_vol16_ch179_p024.jpg", 887, 1300], ["tokyo_ghoul_re_vol16_ch179_p025.jpg", 882, 1300], ["tokyo_ghoul_re_vol16_ch179_p026.jpg", 897, 1300], ["tokyo_ghoul_re_vol16_ch179_p027.jpg", 1794, 1300], ["tokyo_ghoul_re_vol16_ch179_p028.jpg", 898, 1300], ["tokyo_ghoul_re_vol16_ch179_p029.jpg", 894, 1300], ["tokyo_ghoul_re_vol16_ch179_p030.jpg", 888, 1300], ["tokyo_ghoul_re_vol16_ch179_p031.jpg", 883, 1300], ["tokyo_ghoul_re_vol16_ch179_p032.jpg", 1796, 1300], ["tokyo_ghoul_re_vol16_ch179_p033.jpg", 889, 1300], ["tokyo_ghoul_re_vol16_ch179_p034.jpg", 919, 1300], ["tokyo_ghoul_re_vol16_ch179_p035.jpg", 1920, 1080]],
#                         page: 0,
#                         prevChapter: "vol16/ch178/rus",
#                         nextChapter: "",
#                         prefix: ""
#                     });
#                 });
#             </script>"""
#
# test_data = test_script.split()


def is_init_reader(element):
    assert isinstance(element, str)

    token1 = '[['
    token2 = '["'
    return element.startswith(token1) or element.startswith(token2)


def find_init_reader_elements(input_array):
    init_reader_element = filter(is_init_reader, input_array)
    return init_reader_element


def remove_tokens(array: list):
    tokens = ['[["', '["']
    result = []

    for j in array:
        if j.startswith(tokens[0]):
            el = j.replace('",', '').replace(tokens[0], '')
        elif j.startswith(tokens[1]):
            el = j.replace('",', '').replace(tokens[1], '')
        result.append(el)

    return result


def is_href(element):
    assert isinstance(element, str)

    token = '"//'
    return element.startswith(token)


def find_dir_element(array: list):
    dir_element = filter(is_href, array)
    return dir_element


def remove_symbols(element):
    for href in element:
        if href.startswith('"') and href.endswith('",'):
            href = href.replace('"', '')
            result = href.replace(',', '')
            return result


def form_url(array: list, href: str):
    # https://img2.desu.me/manga/rus/tokyo_ghoul_re/vol16_ch179/tokyo_ghoul_re_vol16_ch179_p001.jpg
    result = []

    for link in array:
        result.append(f'https:{href}{link}')

    return result


def script_parser(script_array: list):
    pics = find_init_reader_elements(script_array)
    pics_array = remove_tokens(pics)

    dir_elem = find_dir_element(script_array)
    href = remove_symbols(dir_elem)

    result = form_url(pics_array, href)
    return result
