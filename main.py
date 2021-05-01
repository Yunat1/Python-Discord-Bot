import discord
import os
import requests
import nltk
import nltk.tag.stanford as st
from urllib.request import urlopen
from urllib.parse import unquote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Search Wikipedia article and extract text
#To-do Textfile artiekl
def search_web(keyword):
    #Get and Load Wikipage
    urlStr = 'https://de.wikipedia.org/wiki/' + keyword
    '''
    res = requests.get(urlStr)
    html_page = res.text
    '''
    try:
        html_page = urlopen(urlStr).read()
    except HTTPError:
        return 'Zu diesem Thema gibt es keinen Wikipedia Artikel', []

    soup = BeautifulSoup(html_page, features="html.parser")

    links = []
    count = 0
    text = ''

    #remove tables first (so no text from tables is taken)
    for table in soup.find_all("table"):
        table.decompose()

    #Get first few lines
    for i in soup.find_all('p'):
        if count < 2:
            text += i.getText()
            count += 1
    
    #Remove irrelevant symbols
    for ch in ['\n', '?/i', '\xa0', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]', '[10]', '[11]', '[12]']:
        if ch in text:
            text = text.replace(ch, '')
    
    #Case: empty article
    if 'Artikel verschwunden?' in text:
        return 'Zu diesem Thema gibt es keinen Wikipedia Artikel', []

    #Case: multiple articles
    if len(text) < 130:
        text = 'Zu diesem Thema gibt es keinen Wikipedia Artikel'
        f = open(keyword + ".txt", "w", encoding='utf-8')
        f.write("Meinst du vielleicht eine der folgenden Optionen:" + '\n')
        count = 1

        #mw-content-text
        for link in soup.find_all("a"):
            url = link.get("href", "")
            if "wiktionary" in url:
                break
            if 'Wikipedia:Begriffskl%C3%A4rung' in url:
                break
            if "/wiki/" in url:
                name = url.removeprefix('/wiki/')
                links.append(name)
                enc_name = unquote(name)
                enc_name = enc_name.replace('_', ' ')
                f.write(str(count) + ". " + enc_name + '\n')
                count += 1
        f.close()

    if len(text) > 2000:
        text = text[:2000]

    return text, links

'''
#Check if Message is Person Name
def checkPerson(message):
    tagger = st.StanfordNERTagger('stanford-ner-2015-04-20\classifiers\english.all.3class.distsim.crf.ser.gz', 'stanford-ner.jar')
    for sent in nltk.sent_tokenize(message.content.capitalize()):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = tagger.tag(tokens)
        for tag in tags:
            if tag[1] == 'PERSON':
                return message.content
'''

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

answered = False

@client.event
async def on_message(message):
    global answered

    #Check answer message from user
    def check(m):
        num = len(links)
        test = list(range(1, num  + 1))
        try:
            return int(m.content) in test
        except ValueError:
            print("Input is not a number. Will be ignored")

    if message.author == client.user:
        return
    if message.content.startswith('!'):
        keyword = message.content[1:].replace(' ', '_')
        text, links = search_web(keyword)
        await message.channel.send(text)

        if len(text) < 50 and links:
            await message.channel.send(file=discord.File(keyword + ".txt"))
            msg = await client.wait_for("message", check = check)
            text, links = search_web(links[int(msg.content) - 1])
            await message.channel.send(text)
            os.remove(keyword + ".txt")
    
    if "@" in message.content:
        test = message.role_mentions
        for role in message.guild.roles:
            if test[0].id == role.id:
                for member in role.members:
                    if member != client.user:
                        await member.send("Hallo")


    '''
    if message.author.id == 290938922027057164 and checkPerson(message):
        if not answered:
            await message.channel.send("WER?")
            answered = True
        else:
            await message.channel.send("NEIN wer gefragt hat! HOOOPS")
            answered = False
    '''

client.run(TOKEN)

