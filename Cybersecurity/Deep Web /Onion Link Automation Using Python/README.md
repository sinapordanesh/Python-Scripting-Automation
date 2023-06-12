# Onion Link Automation Using Python

```python
import requests 
import random 
import re

def scrape(newdate):
    yourquery = newdate
	
    if " " in yourquery:
        yourquery = yourquery.replace (" ", "+")
    url = "https://ahmia.fi/search/?q={}".format(yourquery)
    request = requests.get(url)
    content = request.text
    regexquery = "\w+\.onion"
    mineddata = re.findall(regexquery, content)

    n = random.randint(1, 9999)

    filename = "sites{}.txt".format(str(n))
    print("Saving to ... ", filename)
    mineddata = list(dict.fromkeys(mineddata))

    for k in mineddata:
        with open(filename, "a") as newfile:
            k = k + "\n"
            newfile.write(k)
    print("All the files written to a text file : ", filename)

    with open(filename) as input.file:
        head = [next(input_file) for x in range(5)]
        contents = '\n'.join(map(str, head))
        print(contents)

newdata = input("enter query: ")
scrape(newdata)
```

This is a Python script that automates the process of scraping onion links from [https://ahmia.fi/search/](https://ahmia.fi/search/) based on a query input by the user. The script uses the requests module to send an HTTP GET request to the search URL with the user's query. It then extracts all the onion links from the HTML content using a regular expression pattern, and saves them to a text file with a random filename. The script then reads the first 5 lines of the text file and prints them to the console.

To run the script, the user is prompted to input a query, which is then passed as an argument to the `scrape` function. The function replaces any spaces in the query with `+` signs to form a valid URL, and then performs the steps mentioned above.

Overall, this script demonstrates how Python can be used to automate web scraping tasks, and how regular expressions can be used to extract specific data from HTML content.