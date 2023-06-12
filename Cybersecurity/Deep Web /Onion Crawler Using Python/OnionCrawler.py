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
