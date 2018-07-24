import os
from bs4 import BeautifulSoup as BS
import sqlite3

document_root = 'Seaborn.docset/Contents/Resources/Documents'
index_fp = os.path.join(document_root, 'examples/index.html')
tutorial_fp = os.path.join(document_root, 'tutorial.html')
sqlite_fp = 'Seaborn.docset/Contents/Resources/docSet.dsidx'

with open(index_fp, 'r') as infile:
    examples = BS(infile, 'lxml').find('div', {
        'id': 'example-gallery'
    }).find_all('a')[1:]
    gallaries = []  # list of examples, in the format of (name, link)
    dash_str_format = 'examples/{0}'
    for example in examples:
        link = dash_str_format.format(example['href'][2:])
        title = ''
        with open(os.path.join(document_root, link), 'r') as gallery_file:
            title = BS(gallery_file, 'lxml').find('h1').text.replace(
                u'\u2019', '\'').replace(
                    u'\xb6', '')  # dirty hack to get around unicode errors
        name = '{} - {}'.format(example.span.p.text, title)
        gallaries.append((name, link))

with open(tutorial_fp, 'r') as infile:
    tutorials = BS(infile, 'lxml').find('div', {
        'class': 'row'
    }).find_all('a', {'class': 'reference internal'})
    guides = []  # list of guides
    for tutorial in tutorials:
        link = tutorial['href']
        name = tutorial.text
        guides.append((name, link))

with sqlite3.connect(sqlite_fp) as c:
    for item in gallaries:
        c.execute(
            'INSERT OR IGNORE INTO searchIndex(name, type, path) '
            'VALUES (?, ?, ?)', (item[0], 'Sample', item[1]))
    for item in guides:
        c.execute(
            'INSERT OR IGNORE INTO searchIndex(name, type, path) '
            'VALUES (?, ?, ?)', (item[0], 'Guide', item[1]))

print('Finished adding samples and tutorials')
