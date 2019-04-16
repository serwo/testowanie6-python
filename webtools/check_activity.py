from bs4 import BeautifulSoup
import os
import requests


class LinksActivity:
    def __init__(self, directory):
        self.directory = directory

    def __iter__(self):
        self.fileslist = self._get_html_paths(self.directory, [])
        self.linksactivity = self._check_activity(self.fileslist)
        self.pos = -1
        return self

    def __next__(self):
        self.pos += 1
        if self.pos >= len(self.linksactivity):
            raise StopIteration
        return self.linksactivity[self.pos]

    def __str__(self):
        return self

    def _get_html_paths(self, directory, fileslist):
        for root, subdirs, files in os.walk(directory):
            for curfile in files:
                if curfile.endswith(".html"):
                    fileslist.append(os.path.join(root, curfile))
            for subdir in subdirs:
                self._get_html_paths(subdir, fileslist)
        return fileslist

    def _is_valid_page(self, path):
        try:
            return requests.get(path).ok
        except Exception:
            return False

    def _is_file_or_valid_page(self, path):
        return os.path.isfile(path) or self._is_valid_page(path)

    def _check_activity(self, fileslist):
        linkslist = []
        for path in fileslist:
            with open(path) as f:
                soup = BeautifulSoup(f.read(), 'lxml')
                for link in soup.find_all('a'):
                    val = link.get('href')
                    linkslist.append((val, path,
                                      self._is_file_or_valid_page(val)))
                for image in soup.find_all('img'):
                    val = image.get('src')
                    linkslist.append((val, path,
                                      self._is_file_or_valid_page(val)))
        return linkslist


# root = LinksActivity("/home/threaz/Desktop/webtools/html_files")
# for i in root:
#     print(i)
