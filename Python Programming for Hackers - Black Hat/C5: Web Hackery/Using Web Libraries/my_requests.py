import requests

url = 'http://google.com'
response = requests.get(url) # GET

data = {'user': 'tim', 'passwd': '31337'}
response = requests.post(url, data=data) # POST
print(response.text) # response.text = string; response.content = bytestring
