import urllib2


""""
example of how to make a GET request to a website
"""
url = 'https://www.nostarch.com'
response = urllib2.urlopen(url) # GET
print(response.read())
response.close()


""""
how to create the same GET request by using the Request class and by defining a custom User-Agent HTTP header
"""
url = "https://www.nostarch.com"

# define a headers dictionary
headers = {'User-Agent': "Googlebot"}

# create our Request object and pass in the url and the headers dictionary
request = urllib2.Request(url,headers=headers)
# pass the Request object to the urlopen function call
response = urllib2.urlopen(request)

print(response.read())
response.close()