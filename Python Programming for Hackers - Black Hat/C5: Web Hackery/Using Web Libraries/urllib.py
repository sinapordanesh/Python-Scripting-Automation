import urllib.parse
import urllib.request

""""
how to make a GET request
"""
# define the target URL
url = 'http://boodelyboo.com'

# using the urlopen method as a context manager, we make the request
with urllib.request.urlopen(url) as response: # GET

    # read the response
    content = response.read()

print(content)


""""
In this example, the info dictionary contains the credentials (user, passwd) needed to log in to the target website
"""
info = {'user': 'tim', 'passwd': '31337'}
data = urllib.parse.urlencode(info).encode() # data is now of type bytes

req = urllib.request.Request(url, data) # POST request
with urllib.request.urlopen(req) as response: # POST
    content = response.read()
print(content)