import ast
from urllib.parse import urljoin

# script_array = ['<script', 'type="text/javascript">', 'var', 'prevLink', '=', 'false;', 'var', 'nextLink', '=', 'true;',
#                 'var', 'nextChapterLink', '=', '"/eta_farforovaia_kukla_vliubilas/vol1/2";', 'rm_h.initReader(',
#                 '[2,3],',
#                 '[[\'https://h27.rmr.rocks/\',\'\',"auto/28/40/18/001.png_res.jpg?t=1647938574&u=0&h=vG8VQHeCjRjjJiY1lnQ0Kw",900,1280],[\'https://h8.rmr.rocks/\',\'\',"auto/28/40/18/002.png_res.jpg?t=1647938574&u=0&h=urgToMY4IkFolCYDYca1jg",1800,1280],[\'https://h1.rmr.rocks/\',\'\',"auto/28/40/18/003.png_res.jpg?t=1647938574&u=0&h=tRMhRfchw1VSZiWt5GFNBg",900,1280],[\'https://h30.rmr.rocks/\',\'\',"auto/28/40/18/004.png_res.jpg?t=1647938574&u=0&h=15Q18UxASIvVlYiz6DZkWQ",900,1280],[\'https://h11.rmr.rocks/\',\'\',"auto/28/40/18/005.png_res.jpg?t=1647938574&u=0&h=12Hg4LLK8IxZ9oi7g7doNw",900,1280],[\'https://h8.rmr.rocks/\',\'\',"auto/28/40/18/006.png_res.jpg?t=1647938574&u=0&h=qGaXS18xP4IWs4Yizu2rUA",900,1280],[\'https://h27.rmr.rocks/\',\'\',"auto/28/40/18/007.png_res.jpg?t=1647938574&u=0&h=uZyNAzVCfThNs7KIZ6ifBA",900,1280],[\'https://h24.rmr.rocks/\',\'\',"auto/28/40/18/008.png_res.jpg?t=1647938574&u=0&h=SBE9HoSdSMx9QyYwcwJRMw",900,1280],[\'https://h43.rmr.rocks/\',\'\',"auto/28/40/18/009.png_res.jpg?t=1647938574&u=0&h=yHpPmn6AdfzYjv1vyPHc5A",900,1280],[\'https://h31.rmr.rocks/\',\'\',"auto/28/40/18/010.png_res.jpg?t=1647938574&u=0&h=bddXfq_dDprXgXeYAGA6nA",900,1280],[\'https://h30.rmr.rocks/\',\'\',"auto/28/40/18/011.png_res.jpg?t=1647938574&u=0&h=sN8ahKwyhTWzUMNCPp5lzA",900,1280],[\'https://h11.rmr.rocks/\',\'\',"auto/28/40/18/012.png_res.jpg?t=1647938574&u=0&h=hBTboSORDv7xoYLQCtREmQ",900,1280],[\'https://h43.rmr.rocks/\',\'\',"auto/28/40/18/013.png_res.jpg?t=1647938574&u=0&h=x64HhU-AATJPi51hGnOaeA",900,1280],[\'https://h27.rmr.rocks/\',\'\',"auto/28/40/18/014.png_res.jpg?t=1647938574&u=0&h=4BWiT8e0rwNFDY6hnRtISw",900,1280],[\'https://h24.rmr.rocks/\',\'\',"auto/28/40/18/015.png_res.jpg?t=1647938574&u=0&h=tBQIXYySEkYhKCd-bElGmA",900,1280],[\'https://h38.rmr.rocks/\',\'\',"auto/28/40/18/016.png_res.jpg?t=1647938574&u=0&h=x44fpAq07LRvJVvBoZYEug",900,1280],[\'https://h40.rmr.rocks/\',\'\',"auto/28/40/18/017.png_res.jpg?t=1647938574&u=0&h=M881aTe4ZNWXx4V1I4r6Mw",900,1280],[\'https://h30.rmr.rocks/\',\'\',"auto/28/40/18/018.png_res.jpg?t=1647938574&u=0&h=ThFjBYcYDgVbJJNnwOO-8w",900,1280],[\'https://h31.rmr.rocks/\',\'\',"auto/28/40/18/019.png_res.jpg?t=1647938574&u=0&h=glZzJFZo9baW63OIia0R7g",900,1280],[\'https://h43.rmr.rocks/\',\'\',"auto/28/40/18/020.png_res.jpg?t=1647938574&u=0&h=tJRe_S3jTo1MZIy55hAB6w",900,1280],[\'https://h40.rmr.rocks/\',\'\',"auto/28/40/18/021.png_res.jpg?t=1647938574&u=0&h=LasGjoOjYh3VVstnlyMgyg",900,1280],[\'https://h42.rmr.rocks/\',\'\',"auto/28/40/18/022.png_res.jpg?t=1647938574&u=0&h=ZA12nrr_3L-_Hg82uqbcqw",900,1280],[\'https://h38.rmr.rocks/\',\'\',"auto/28/40/18/023.png_res.jpg?t=1647938574&u=0&h=4obkr8-sSdthYh81GFdkKw",900,1280],[\'https://h1.rmr.rocks/\',\'\',"auto/28/40/18/024.png_res.jpg?t=1647938574&u=0&h=Wh0vSRsrUNZ-5--O1UySfA",900,1280],[\'https://h30.rmr.rocks/\',\'\',"auto/28/40/18/025.png_res.jpg?t=1647938574&u=0&h=fA8JGJFoIYiTr6ie5rHinQ",900,1280],[\'https://h31.rmr.rocks/\',\'\',"auto/28/40/18/026.png_res.jpg?t=1647938574&u=0&h=6ZYZr5wFqvL6xOt2elFlbg",900,1280],[\'https://h42.rmr.rocks/\',\'\',"auto/28/40/18/027.png_res.jpg?t=1647938574&u=0&h=EvZQqjiDUpYKgLpGjHVeWA",900,1280],[\'https://h40.rmr.rocks/\',\'\',"auto/28/40/18/028.png_res.jpg?t=1647938574&u=0&h=iSUxh29LKtpV9ldQNDhvyQ",900,1280],[\'https://h38.rmr.rocks/\',\'\',"auto/28/40/18/029.png_res.jpg?t=1647938574&u=0&h=TVmWgkue0CwTXRlcWjI8Eg",900,1280],[\'https://h31.rmr.rocks/\',\'\',"auto/28/40/18/030.png_res.jpg?t=1647938574&u=0&h=GOKcuNii7QFOk8PLo62ejA",900,1280],[\'https://h1.rmr.rocks/\',\'\',"auto/28/40/18/031.png_res.jpg?t=1647938574&u=0&h=DYnni5MsDYgU59l57Fdylw",900,1280],[\'https://h30.rmr.rocks/\',\'\',"auto/28/40/18/032.png_res.jpg?t=1647938574&u=0&h=O5V9CJhgVulQCZrPfc_HXA",900,1280],[\'https://h11.rmr.rocks/\',\'\',"auto/28/40/18/033.png_res.jpg?t=1647938574&u=0&h=4mVCYVpLl-es-QwR0KVsXw",900,1280],[\'https://h43.rmr.rocks/\',\'\',"auto/28/40/18/034.png_res.jpg?t=1647938574&u=0&h=yAqFjRFCPVSaG2dqtbdsbA",900,1280],[\'https://h27.rmr.rocks/\',\'\',"auto/28/40/18/035.png_res.jpg?t=1647938574&u=0&h=vguyxnPGuF-4-O0u6_q6ug",900,1280],[\'https://h43.rmr.rocks/\',\'\',"auto/28/40/18/036.png_res.jpg?t=1647938574&u=0&h=5zX1o1Cs4gWzVdqEWpfmSQ",900,1280],[\'https://h24.rmr.rocks/\',\'\',"auto/28/40/18/037.png_res.jpg?t=1647938574&u=0&h=tGN72vo_dX9gMTdivQNV8w",900,1280],[\'https://h2.rmr.rocks/\',\'\',"auto/28/40/18/038.png_res.jpg?t=1647938574&u=0&h=XGhjUydQCdjWCU5XScOz-g",900,1280],[\'https://h8.rmr.rocks/\',\'\',"auto/28/40/18/039.png_res.jpg?t=1647938574&u=0&h=VmisY09y4gShEXXLDwG7tQ",1800,1280],[\'https://h24.rmr.rocks/\',\'\',"auto/28/40/18/040.png_res.jpg?t=1647938574&u=0&h=TctGaXbBGWDIl7q8T-UEzA",900,1280],[\'https://h43.rmr.rocks/\',\'\',"auto/28/40/18/041.png_res.jpg?t=1647938574&u=0&h=H8hr4-ZBEsvTwbADKRMl6Q",900,1280],[\'https://h27.rmr.rocks/\',\'\',"auto/28/40/18/042.png_res.jpg?t=1647938574&u=0&h=YvuFSyzir8b4LdRbgIXk3Q",1800,1280],[\'https://h42.rmr.rocks/\',\'\',"auto/28/40/18/043.png_res.jpg?t=1647938574&u=0&h=UJJ93NLHV4BdklBc0QjcKw",900,1280],[\'https://h11.rmr.rocks/\',\'\',"auto/28/40/18/044.png_res.jpg?t=1647938574&u=0&h=z4pfBf8iVdiTXXNOPlvgKg",900,1280],[\'https://h2.rmr.rocks/\',\'\',"auto/28/40/18/045.png_res.jpg?t=1647938574&u=0&h=mWUXXJH6dyG3NAvrtOfwCw",1800,1280],[\'https://h8.rmr.rocks/\',\'\',"auto/28/40/18/046.png_res.jpg?t=1647938574&u=0&h=V5dSy8XZGy1QQ1pccabm7w",900,1280],[\'https://h31.rmr.rocks/\',\'\',"auto/28/40/18/047.png_res.jpg?t=1647938574&u=0&h=GkIOX6jFLKG3wvAfESV16w",900,1169]],',
#                 '0,', 'false,',
#                 '[{"path":"https://h43.rmr.rocks/","res":true},{"path":"https://h8.rmr.rocks/","res":true},{"path":"https://h1.rmr.rocks/","res":true},{"path":"https://h40.rmr.rocks/","res":true},{"path":"https://h27.rmr.rocks/","res":true},{"path":"https://h2.rmr.rocks/","res":true},{"path":"https://h30.rmr.rocks/","res":true},{"path":"https://h42.rmr.rocks/","res":true},{"path":"https://h24.rmr.rocks/","res":true},{"path":"https://h11.rmr.rocks/","res":true},{"path":"https://h31.rmr.rocks/","res":true},{"path":"https://h38.rmr.rocks/","res":true}],',
#                 'false);', '</script>']


def isInitReader(element):
    assert (type(element) is str)
    # token1 = "rm_h.initReader"
    token2 = "[["
    return element.startswith(token2)


def find_init_reader_elements(input_array):
    init_reader_element = filter(isInitReader, input_array)
    return init_reader_element


def print_array(array_with_images, name='Lalala'):
    print("#####", name)
    for a in array_with_images:
        print(a)


def to_multi_array(multir_array_string_representation):
    # for some reason parsed in tuple with single element
    parsed = ast.literal_eval(multir_array_string_representation)
    # print(type(parsed), type(parsed[0]))
    return parsed[0]


def to_object(element):
    # element is an array which looks like ['https://h31.rmr.rocks/', '', 'auto/28/40/18/047.png_res.jpg?t=1647938574&u=0&h=GkIOX6jFLKG3wvAfESV16w', 900, 1169]
    offset = 1 if len(element) == 5 and element[1] == '' else 0
    pos_image_part_1 = 0
    pos_image_part_2 = 1 + offset
    pos_width = 2 + offset
    pos_height = 3 + offset
    # print(element)
    return {
        "width": element[pos_width],
        "height": element[pos_height],
        "full_url": urljoin(element[pos_image_part_1], element[pos_image_part_2])
    }


def to_array_with_objects(multi_array):
    return [to_object(e) for e in multi_array]


def main(script_array):
    el = find_init_reader_elements(script_array)
    filtered_list = list(el)
    multi_array = to_multi_array(filtered_list[0])
    result = to_array_with_objects(multi_array)
    # print_array(result, "FINAL")
    return result


