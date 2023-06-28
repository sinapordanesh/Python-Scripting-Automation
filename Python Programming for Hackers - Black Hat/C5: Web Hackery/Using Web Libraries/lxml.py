""""
Suppose you have the HTML content from a request stored in a variable
named content. Using lxml, you could retrieve the content and parse the links
as follows
"""

from io import BytesIO
from lxml import etree

import requests
url = 'https://nostarch.com2' 
r = requests.get(url) # GET
content = r.content # content is of type 'bytes'

parser = etree.HTMLParser()

# The BytesIO class enables us to use the returned byte string content as a file-like object to pass to the lxml parser
content = etree.parse(BytesIO(content), parser=parser) # Parse into tree
# simple query -> find tags -> contains links
for link in content.findall('//a'): # find all "a" anchor elements.
	print(f"{link.get('href')} -> {link.text}")