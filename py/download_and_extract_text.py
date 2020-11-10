"""
For downloading and extracting the text itself from a html file.

TODO:   Save down the text in some useful format. 
        Add some nice messaging.
        Add some defenses (what if the url is invalid?)
        Does it matter that it is a htm file?
"""
import os, sys
import datetime as dt
from urllib.request import urlopen
from bs4 import BeautifulSoup

proj_dir = os.path.join(os.environ.get('HOME'), 'Moby_Dick_Stats')
txt_dir = os.path.join(proj_dir, 'txt')

url = 'https://www.gutenberg.org/files/2701/2701-h/2701-h.htm'
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = ' '.join(chunk for chunk in chunks if chunk)

moby_dick_txt_file = os.path.join(txt_dir, 'moby_dick.txt')
with open(moby_dick_txt_file, 'w') as f:
    f.write(text)

print(dt.datetime.now().isoformat() + ' INFO: ' + moby_dick_txt_file + ' saved.')
