from bs4 import BeautifulSoup
import os
import requests


class FindLinks:
    def __init__(self, link):
        self.link = link

    def __iter__(self):
        self.linkslist = self._find_links(self.link)
        self.pos = -1
        return self

    def __next__(self):
        self.pos += 1
        if self.pos >= len(self.linkslist):
            raise StopIteration
        return self.linkslist[self.pos]

    def _find_links(self, link):
        if os.path.isfile(link):
            with open(link) as f:
                text = f.read()
                return self._search_in_file(text, link)
        try:
            if requests.get(link).ok:
                return self._search_in_file(requests.get(link).text, link)
        except Exception:
            return None

    def _search_in_file(self, text, path):
        linkonwebs = []
        soup = BeautifulSoup(text, 'lxml')
        for link in soup.find_all('a'):
            val = link.get('href')
            try:
                if requests.get(val).ok:
                    if self._find_root_link(val, path):
                        linkonwebs.append(val)
            except Exception:
                continue
        return linkonwebs

    def _find_root_link(self, link, root):
        htmlfile = requests.get(link).text
        soup = BeautifulSoup(htmlfile, 'lxml')
        for link in soup.find_all('a'):
            if link.get('href') == root:
                return True


# root = FindLinks("https://www.ebeactive.pl/")
# for i in root:
#     print(i)

# root2 = FindLinks('/home/threaz/Desktop/webtools/html_files/file0_1.html')
# for j in root2:
#     print(j)