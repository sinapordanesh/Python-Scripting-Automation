# Telegram Bot for Scraping Onion Links

```python
import requests 
import re, random 
import telebot

BOT_TOKEN = '' #add your bot token here

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello']) 
def send_welcome(message):
    bot.reply_to(message, """Welcome to Dark Web OSINT/darkweb (search) Example: /darkweb credit cards Created By Sina 
                            """)
    
@bot.message_handler(commands=['darkweb', 'getonions'])
def send_welcome(message):
    bot.reply_to(message,"[+] Getting Links")
    data=message.text 
    newdata=data.replace('/darkweb')
    bot.reply_to(message, scrape(newdata))
    bot.reply_to(message,"[!] You Need TOR To Access ninon Links")

def scrape(newdata):
    yourquery =newdata
    #yourquery - "Croatia Index Of"

    if " " in yourquery:
        yourquery = yourquery.replace (" ", "+")
    url = "https://ahmia.fi/search/?q={}".format (yourquery)
    request = requests.get(url)
    content = request.text
    regexquery = "\w+\.onion"
    mineddata = re.findall(regexquery, content)

    n = random.randint(1, 9999)

    filename = "sites{}.txt".format(str(n))
    print("Saving to ...", filename)
    mineddata = list(dict.fromkeys(mineddata))

    with open(filename, "w+") as _:
        print ("")
    for k in mineddata:
        with open(filename,"a") as newfile:
            K = K+ "\n"
            newfile.write(k)
    print ("All the files written to a text file : ", filename)

    with open(filename) as input_file:
        head = [next(input_file)for _ in range (7)]
        contents= '\n'.join(map(str, head)) 
        print (contents)

    return contents

bot.infinity_polling()
```

This code block contains Python code for a Telegram bot that can be used to automate the process of scraping onion links from [https://ahmia.fi/search/](https://ahmia.fi/search/) using the `scrape` function from the first code block in this document.

The bot uses the `telebot` library to interface with the Telegram API. When a user sends a message to the bot with the `/darkweb` command followed by a query, the bot calls the `scrape` function with the query and returns the first 7 onion links found in the search results.

To use the bot, the user must first obtain a bot token and add it to the `BOT_TOKEN` variable in the code. The bot can then be run on a server or local machine to handle incoming messages from Telegram users.

Overall, this code demonstrates how Python can be used to automate web scraping tasks and how the `telebot` library can be used to create custom bots that interface with the Telegram API.