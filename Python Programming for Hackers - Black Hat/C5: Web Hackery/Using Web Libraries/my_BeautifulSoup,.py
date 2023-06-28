from bs4 import BeautifulSoup as bs
import requests

url = 'http://bing.com'
r = requests.get(url)

# parse the content into a tree
tree = bs(r.text, 'html.parser') 
# iterate over the links
for link in tree.find_all('a'): # find all "a" anchor elements.
    print(f"{link.get('href')} -> {link.text}")