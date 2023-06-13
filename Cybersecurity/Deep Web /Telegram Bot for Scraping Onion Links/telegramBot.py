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
