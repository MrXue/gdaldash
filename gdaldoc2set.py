#coding=utf-8

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag

conn = sqlite3.connect('C:/Users/xuexianguang/AppData/Local/Zeal/Zeal/docsets/GDAL.docset/Contents/Resources/docSet.dsidx')
cur = conn.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'C:/Users/xuexianguang/AppData/Local/Zeal/Zeal/docsets/GDAL.docset/Contents/Resources/Documents'

page = open(os.path.join(docpath,'annotated.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 1:
        path = tag.attrs['href'].strip()
        if path != 'annotated.html':
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Class', path))
            print('name: {}, path: {}'.format(name, path))

conn.commit()
conn.close()