
# Onion Crawler Using Python

```python
import requests 
import csv 
import re 
import time

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9051'}
    return session

def public_test():
    # Regex pattern for matching numbers
    pattern = "(?:[0-9]{4}-){3}[0-9]{4}|[0-9]{16}"
    # URLs of the websites to crawl
    urls = ['pastebin.com/diff/E34JsqAy', 'pastebin.pl/view/0f9e7cc4']
    # Loop through the URLs and fetch the HTML content
    for url in urls:
        response = requests.get("http://{}".format(url), timeout=25)
        response.close()
        html_content = response.content

        # Search for the regex pattern in the HTML content

        matches = re.findall(pattern, html_content.decode("ISO-8859-1"))

        # Output the matching numbers
        print ("Matching numbers on {}:".format(url))
        for match in matches:
            print (match)
        with open('scraped_data.csv', mode='a') as file:
            writer = csv.writer(file)
            for match in matches:
                writer.writerow([match])

def onion_test(filename):
    # Regex pattern for matching numbers
    pattern = "(?:[0-9]{4}-){3}[0-9]{4}|[0-9]{16}"
    # URLs of the websites to crawl
    data = [line.strip() for line in open(filename, 'r')]
    urls = data
    # Loop through the URLs and fetch the HTML content
    for url in urls:
        time.sleep(5)
        try:
            response = darksession.get("http://{}".format(url), timeout=25)
            response.close()
            html_content = response.content
        except requests. ConnectionError:
            continue

        # Search for the regex pattern in the HTML content

        matches = re.findall(pattern, html_content.decode("ISO-8859-1"))

        # Output the matching numbers
        print("Matching numbers on {}:".format(url))
        for match in matches:
            print (match)
        with open('scraped_data.csv', mode='a') as file:
            writer = csv.writer(file)
            for match in matches:
                writer.writerow([match])

filename = input("Enter file of websites name: ")

#For public test, connent prints and onion_test(). For onion_test(), just comment public_test().  
print("Connecting To TOR")
darksession=get_tor_session()
print ("New IP Address is: {}".format(darksession.get("http://httpbin.org/in").text))
onion_test(filename)
#public_test()
```

The `onion_test` function crawls onion sites using a TOR proxy. It first reads in a list of onion URLs from a file. It then loops through each URL, sends an HTTP GET request to the site using the TOR proxy, and extracts all the matching numbers from the HTML content using a regular expression pattern. The function then prints the matching numbers to the console and appends them to a CSV file called `scraped_data.csv`.

The purpose of using a TOR proxy is to keep the user's IP address hidden and to make it difficult for the site to track the user's behavior. The 5-second sleep timer between each request is included to prevent the user from getting blocked by the site, as frequent requests could be seen as suspicious behavior. If a connection error occurs, the function simply moves on to the next URL.

The final functionality of the code is to crawl onion sites and extract specific data from the HTML content of these sites using regular expressions. This functionality can be useful for a variety of purposes, such as scraping data for research or analysis. However, it is important to note that web scraping can be illegal or unethical in certain situations, so it should be used responsibly and with caution.

- To run this code we need the `Onion Link Automation Using Python` code run before and pass the result of that code as the “website names file” when we run this code.
- May need to check your Tor proxy configs and make sure all ports numbers are correct