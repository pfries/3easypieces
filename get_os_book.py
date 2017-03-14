#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests, os, subprocess
from collections import OrderedDict

if __name__ == '__main__':
    base_url = 'http://pages.cs.wisc.edu/~remzi/OSTEP/'
    html = requests.get(base_url)
    soup = BeautifulSoup(html.text, 'html.parser')
    links = {}
    for link in soup.find_all('a'):
        value = link.get('href')
        if value and value.endswith('pdf'):
            parent = link.find_parent("td")
            chapter_num = parent.find_all("small")
            if(chapter_num):
                num = chapter_num[0].contents[0]
                key = "%02d" % (int(num),)
                links[key] = value
            else:
                if value == 'preface.pdf':
                    links['000'] = value
                if value == 'toc.pdf':
                    links['001'] = value
    ordered = OrderedDict(sorted(links.items()))

    output_path = 'output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for chpt,resource in ordered.items():
        response = requests.get(base_url + resource)
        with open('{0}/{1}_{2}'.format(output_path, chpt, resource), 'wb') as f:
            f.write(response.content)
    owd = os.getcwd()
    os.chdir(output_path)
    proc = subprocess.Popen('pdftk *.pdf cat output operating_systems_three_easy_pieces.pdf', shell=True)
    os.chdir(owd)
    
