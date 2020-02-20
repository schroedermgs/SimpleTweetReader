"""A program that can read tweets from Twitter.com out loud."""

print("Importing modules... Please wait... _\|/_\|/_\|/_\|/_\|/_\|/_ ")
import translate
import pyttsx3 as tx
from bs4 import BeautifulSoup as soup 
import bs4
import datetime as dt
import selenium
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
print("Done. \n \n")

timeline = input("WHOSE TWITTER TIMELINE WOULD YOU LIKE TO HEAR? \nPlease type in a valid public username. \n\n")\
.replace('@','').replace('#','').replace('/','').replace(' ','')

if len(timeline)==0:
    input("You may have to login using the browser. \nPress <ENTER> to continue. \n\n")

print("Launching Internet browser... Please wait... _\|/_\|/_\|/_\|/_\|/_\|/_ ")
url = "https://twitter.com/" + timeline
try:
    br1 = webdriver.Chrome('C:/chromedriver.exe')
except:
    input("SORRY, YOU MUST INSTALL THE GOOGLE CHROME WEBDRIVER IN YOUR C DRIVE (C:/chromedriver.exe) IN ORDER TO PROCEED. ")
time.sleep(1)
br1.get(url)
time.sleep(5)
height = br1.execute_script("return document.body.scrollHeight")
print("Done. \n \n")

num = input("HOW MANY SCROLL-BACKS? \nInput 0 to 10 page-loads (for more tweets): ")
if len(num)==0:
    num=0

print("Scrolling and loading... Please wait... _\|/_\|/_\|/_\|/_\|/_\|/_  ")
try: 
    if 0<=int(num)<=10:
        for i in range(int(num)):
            time.sleep(1.1)
            br1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.0)
            if i==round(int(num)/2):
                print("                                        _\|/_\|/_\|/_\|/_\|/_\|/_")
    else: 
        input("Invalid input. Proceeding with no scroll-back. \nPress <ENTER> to continue. \n\n")
except:
    input("Invalid input. Proceeding with no scroll-back. \nPress <ENTER> to continue. \n\n")
print("Done. \n \n")

print("Grabbing tweets... Please wait... _\|/_\|/_\|/_\|/_\|/_\|/_ ")
souppage = soup(br1.page_source,'lxml')
tweets = souppage.findAll("div",{"class":"tweet"})

if len(timeline)==0:
    try:
        tweets.pop()
    except:
        input("Invalid input. Program only works for Twitter (https://twitter.com). \n")

datestimes = [tweets[i].find("a",{"class":"tweet-timestamp"})['title'].split(" - ") for i in range(len(tweets))]
fullnames = [tweets[i].find("span",{"class":"FullNameGroup"}).find("strong",{"class":"fullname"}).text for i in range(len(tweets))]
usernames = [tweets[i].find("span",{"class":"username"}).text for i in range(len(tweets))]
verified = [tweets[i].find("span",{"class":"UserBadges"}).text for i in range(len(tweets))]
languages = [tweets[i].find("p",{"class":"tweet-text"})['lang'] for i in range(len(tweets))]

for i,v in enumerate(verified):
    if v=='':
        verified[i]=False
    else:
        verified[i]=True
print("Done: %s tweets. \n \n"%len(tweets))

print("Processing information... Please wait... _\|/_\|/_\|/_\|/_\|/_\|/_ ")
texts = []
quoted = []
for i in range(len(tweets)):
    stringlist = []
    ifretweets = []
    for y in tweets[i].find("p").children:
        if isinstance(y,bs4.element.NavigableString):
            if '%s Retweeted ' %fullnames[i] in y:
                ifretweets.append(str(y).strip())
            else:
                ifretweets.append('')
    quoted.append(''.join(ifretweets))
    for x in tweets[i].find("p",{"class":"tweet-text"}).children:
        if isinstance(x,bs4.element.NavigableString):
            stringlist.append(str(x).strip())
        if isinstance(x,bs4.element.Tag):
            stringlist.append(x.text.strip().replace('#',''))
    texts.append('; '.join(stringlist))
newlist = \
 [ ' '.join([w for w in texts[i].split() if 'http:' not in w and 'https:' not in w \
 and '\xa0' not in w and '.com/' not in w and '.org/' not in w and '.net/' not in w and w.count('/')<=2] ) \
 for i in range(len(tweets)) ]
links = \
 [ ' '.join([w for w in texts[i].split() if 'http:' in w or 'https:' in w or 'www.' in w \
 or '\xa0' in w or '.com' in w or '.org' in w or '.net' in w or w.count('/')>2] ) \
 for i in range(len(tweets)) ] 
texts = newlist
langcodes = {'ar':'arabic','en':'english','es':'spanish','fr':'french','af':'afrikaans', \
            'sq':'albanian','am':'amharic','hy':'armenian','bn':'bengali','cs':'czech', \
            'zh':'chinese','cn':'chinese','zh-cn':'chinese','de':'german','nl':'dutch', \
            'el':'greek','eo':'esperanto','et':'estonian','fa':'persian','ka':'georgian', \
            'ga':'irish','ht':'haitian','he':'hebrew','ha':'hausa','hi':'hindi','rm':'romansh', \
            'is':'icelandic','id':'indonesian','it':'italian','ja':'japanese','ki':'gikuyu', \
            'rw':'kinya rwandan','kg':'congolese','la':'latin','ms':'malay','mg':'malagasy', \
            'mn':'mongolian','my':'burmese','ne':'nepali','no':'norwegian','pt':'portuguese', \
            'pl':'polish','qu':'quechua','ro':'romanian','ru':'russian','sa':'sanskrit', \
            'sk':'slovak','sl':'slovenian','so':'somali','sr':'serbian','sw':'swahili','da':'danish', \
            'sv':'swedish','tl':'filipino tagalog','th':'thai','bo':'tibetan','tr':'turkish', \
            'ug':'uyghur','uk':'ukrainian','ur':'urdu','uz':'uzbek','vi':'vietnamese', \
            'yi':'yiddish','yo':'yoruba','zu':'zulu','fi':'finnish','ko':'korean','km':'khmer'}

interactions = [[f.text for f in tweets[i].findAll("span",{"class":"ProfileTweet-actionCountForAria"})] for i in range(len(tweets))]
media = []

for i in range(len(tweets)):
    temps = []
    if len(tweets[i].findAll("div",{"class":"AdaptiveMedia-videoContainer"}))!=0:
        temps.append('Video')
    if len(tweets[i].findAll("div",{"class":"AdaptiveMedia-photoContainer"}))!=0:
        temps.append('Photo')
    if len(tweets[i].findAll("div",{"class":"QuoteTweet-container"}))!=0:
        temps.append('Quote')
    if len(tweets[i].findAll("div",{"class":"card2"}))!=0:
        temps.append('Hotlink')
    else:
        temps.append('')
    media.append(' '.join(temps))
    
hotlink = []
for i in range(len(tweets)):
    hotempty = []
    try:
        hotempty.append('https://twitter.com'+tweets[i].find("div",{"class":"js-macaw-cards-iframe-container"})['data-full-card-iframe-url'])
    except:
        hotempty.append('')
    hotlink.append(' '.join(hotempty))

headlines = []
summaries = []
for i in range(len(tweets)):
    if len(hotlink[i])!=0:
        br1.get(hotlink[i])
        linkpage = soup(br1.page_source,'lxml')
        try:
            headlines.append( linkpage.find("h2",{"class":"TwitterCard-title"}).text )
        except:
            headlines.append('')
        try:
            summaries.append( linkpage.find("p",{"class":"tcu-resetMargin"}).text + '; etc. etc.' )
        except:
            summaries.append('')
    else:
        headlines.append('')
        summaries.append('')
quoteverify = []

for i in range(len(tweets)):
    try:
        quoteverify.append(str(tweets[i].find("div",{"class":"QuoteTweet-authorAndText"}).find("span",{"class":"UserBadges"}).text))
    except:
        quoteverify.append('NA')

for i,v in enumerate(quoteverify):
    if len(v)==0:
        quoteverify[i]=False
    elif len(v)>6:
        quoteverify[i]=True
    elif len(v)==2:
        quoteverify[i]=None
    else:
        quoteverify[i]=None
        
quotelangs = []
fullquotes = []
quotenames = []

for i in range(len(tweets)):
    try:
        quotelink = 'https://twitter.com' + tweets[i].find("div",{"class":"QuoteTweet-innerContainer"})['href']
    except:
        quotelink = ''
        quotelangs.append('')
        fullquotes.append('')
        quotenames.append('')
    
    if len(quotelink)!=0:
        br1.get(quotelink)
        quotepage = soup(br1.page_source,'lxml')
        try:
            quotelangs.append( quotepage.find("p",{"class":"TweetTextSize--jumbo"})['lang'] )
            quotenames.append( quotepage.find("div",{"class":"content clearfix"}).find("span",{"class":"username"}).text )
            stringlist = []
            for x in quotepage.find("p",{"class":"TweetTextSize--jumbo"}).children:
                if isinstance(x,bs4.element.NavigableString):
                    stringlist.append(str(x).strip())
                if isinstance(x,bs4.element.Tag):
                    stringlist.append(x.text.strip().replace('#',''))
            fullquotes.append('; '.join(stringlist))
        except:
            quotelangs.append('')
            fullquotes.append('')
            quotenames.append('')

fullquotes = \
 [ ' '.join([w.replace('#','') for w in fullquotes[i].split() if 'http:' not in w and 'https:' not in w \
 and '\xa0' not in w and '.com/' not in w and '.org/' not in w and '.net/' not in w and w.count('/')<=2] ) \
 for i in range(len(tweets)) ] 
print("Done. \n \n")

closing = input("CLOSE THE BROWSER? \nAny key submit = 'YES'; <ENTER> = 'NO'. \n\n")
if len(closing)!=0:
    try:
        br1.close()
    except:
        pass
else:
    try:
        br1.get(url)
    except:
        input("Sorry, something went wrong. Press <ENTER> to continue. \n\n")


YesNo = input("EXTRA DETAILS SUCH AS 'LIKE' AND 'RETWEET' STATS? \nAny key submit = 'YES'; <ENTER> = 'NO'. ")

print("Preparing your text... Please wait...  _\|/_\|/_\|/_\|/_\|/_\|/_ ")
TweetReaderText1 = []
TweetReaderText2 = []

months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

for i in range(len(tweets)):
    TemporaryList1 = []
    TemporaryList2 = []
    d = int(datestimes[i][1].split()[0])
    m = int(months[datestimes[i][1].split()[1]])
    y = int(datestimes[i][1].split()[2])
    weekday = days[dt.datetime(y,m,d).weekday()]
    
    if media[i]=='':
        if verified[i]==True:
            TemporaryList1.append("The following from the verified account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        else:
            TemporaryList1.append("The following from account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        TemporaryList1.append(weekday + ', ' + datestimes[i][1] + ' at ' + datestimes[i][0] + '. ')
        TemporaryList2.append('')
        if languages[i]=='en':
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]=='und':
            TemporaryList1.append("Text language blank or undefined!")
            TemporaryList2.append('')
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]!='en' and languages[i]!='und':
            try:
                PreSentence = "Translating from " + langcodes[languages[i]] + "!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            except:
                PreSentence = "Translating from a foreign language!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            try:
                t = translate.Translator(from_lang=languages[i],to_lang='en')
                if 'AN INVALID SOURCE LANGUAGE' in t.translate(texts[i]):
                    TemporaryList1.append("Translator had some trouble translating.")
                    TemporaryList2.append('')
                    TemporaryList2.append(texts[i].replace('@',''))
                    TemporaryList1.append('')
                else:
                    TemporaryList2.append(t.translate(texts[i]).replace('@',''))
                    TemporaryList1.append('')
            except:
                TemporaryList1.append("Translator had some trouble translating.")
                TemporaryList2.append('')
                TemporaryList2.append(texts[i].replace('@',''))
                TemporaryList1.append('')
        if len(YesNo)>0:
            TemporaryList1.append(interactions[i][0] + ', ' + interactions[i][1] + ', ' + interactions[i][2] + '.')
            TemporaryList2.append('')
    
            
    if 'Quote' in media[i]:
        TemporaryList1.append(" %s quoted "%usernames[i].replace('@','') + " the " + "verified"*(quoteverify[i]==True) + 
                              " account, %s"%quotenames[i].replace('@','') + ", who said: ") 
        TemporaryList2.append('')
        if quotelangs[i]=='en':
            TemporaryList2.append(fullquotes[i].replace('@',''))
            TemporaryList1.append('')
        if quotelangs[i]=='und':
            TemporaryList1.append("Text blank or undefined!")
            TemporaryList2.append('')
            TemporaryList2.append(fullquotes[i].replace('@',''))
            TemporaryList1.append('')
        if quotelangs[i]!='en' and quotelangs[i]!='und':
            try:
                PreSentence = "Translating from " + langcodes[quotelangs[i]] + "!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            except:
                PreSentence = "Translating from a foreign language!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            try:
                t = translate.Translator(from_lang=quotelangs[i],to_lang='en')
                if 'AN INVALID SOURCE LANGUAGE' in t.translate(fullquotes[i]):
                    TemporaryList1.append("Translator had some trouble translating.")
                    TemporaryList2.append('')
                    TemporaryList2.append(fullquotes[i].replace('@',''))
                    TemporaryList1.append('')
                else:
                    TemporaryList2.append(t.translate(fullquotes[i]).replace('@',''))
                    TemporaryList1.append('')
            except:
                TemporaryList1.append("Translator had some trouble translating.")
                TemporaryList2.append('')
                TemporaryList2.append(fullquotes[i].replace('@',''))
                TemporaryList1.append('')
        TemporaryList1.append("On " + weekday + ', ' + datestimes[i][1] + " at " + datestimes[i][0] + 
                              ", %s replied to %s: "%(usernames[i].replace('@',''),quotenames[i].replace('@','')))
        TemporaryList2.append('')
        if languages[i]=='en':
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]=='und':
            TemporaryList1.append("Text blank or undefined!")
            TemporaryList2.append('')
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]!='en' and languages[i]!='und':
            try:
                PreSentence = "Translating from " + langcodes[languages[i]] + "!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            except:
                PreSentence = "Translating from a foreign language!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            try:
                t = translate.Translator(from_lang=languages[i],to_lang='en')
                if 'AN INVALID SOURCE LANGUAGE' in t.translate(texts[i]):
                    TemporaryList1.append("Translator had some trouble translating.")
                    TemporaryList2.append('')
                    TemporaryList2.append(texts[i].replace('@',''))
                    TemporaryList1.append('')
                else:
                    TemporaryList2.append(t.translate(texts[i]).replace('@',''))
                    TemporaryList1.append('')
            except:
                TemporaryList1.append("Translator had some trouble translating.")
                TemporaryList2.append('')
                TemporaryList2.append(texts[i].replace('@',''))
                TemporaryList1.append('')
        if len(YesNo)>0:
            TemporaryList1.append(interactions[i][0] + ', ' + interactions[i][1] + ', ' + interactions[i][2] + '.')
            TemporaryList2.append('')
    
    
    if 'Photo' in media[i]:
        if verified[i]==True:
            TemporaryList1.append("The following from the verified account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        else:
            TemporaryList1.append("The following from account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        TemporaryList1.append(weekday + ', ' + datestimes[i][1] + ' at ' + datestimes[i][0] + '. ')
        TemporaryList2.append('')
        TemporaryList1.append("%s displayed some photos. "%usernames[i].replace('@',''))
        TemporaryList2.append('')
        if languages[i]=='en':
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]=='und':
            TemporaryList1.append("Text blank or undefined!")
            TemporaryList2.append('')
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]!='en' and languages[i]!='und':
            try:
                PreSentence = "Translating from " + langcodes[languages[i]] + "!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            except:
                PreSentence = "Translating from a foreign language!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            try:
                t = translate.Translator(from_lang=languages[i],to_lang='en')
                if 'AN INVALID SOURCE LANGUAGE' in t.translate(texts[i]):
                    TemporaryList1.append("Translator had some trouble translating.")
                    TemporaryList2.append('')
                    TemporaryList2.append(texts[i].replace('@',''))
                    TemporaryList1.append('')
                else:
                    TemporaryList2.append(t.translate(texts[i]).replace('@',''))
                    TemporaryList1.append('')
            except:
                TemporaryList1.append("Translator had some trouble translating.")
                TemporaryList2.append('')
                TemporaryList2.append(texts[i].replace('@',''))
                TemporaryList1.append('')
        TemporaryList1.append("Images displayed. ")
        TemporaryList2.append('')
        if len(YesNo)>0:
            TemporaryList1.append(interactions[i][0] + ', ' + interactions[i][1] + ', ' + interactions[i][2] + '.')
            TemporaryList2.append('')
    
    
    if 'Video' in media[i]:
        if verified[i]==True:
            TemporaryList1.append("The following from the verified account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        else:
            TemporaryList1.append("The following from account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        TemporaryList1.append(weekday + ', ' + datestimes[i][1] + ' at ' + datestimes[i][0] + '. ')
        TemporaryList2.append('')
        TemporaryList1.append("%s displayed a video. "%usernames[i].replace('@',''))
        TemporaryList2.append('')
        if languages[i]=='en':
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]=='und':
            TemporaryList1.append("Text blank or undefined!")
            TemporaryList2.append('')
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]!='en' and languages[i]!='und':
            try:
                PreSentence = "Translating from " + langcodes[languages[i]] + "!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            except:
                PreSentence = "Translating from a foreign language!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            try:
                t = translate.Translator(from_lang=languages[i],to_lang='en')
                if 'AN INVALID SOURCE LANGUAGE' in t.translate(texts[i]):
                    TemporaryList1.append("Translator had some trouble translating.")
                    TemporaryList2.append('')
                    TemporaryList2.append(texts[i].replace('@',''))
                    TemporaryList1.append('')
                else:
                    TemporaryList2.append(t.translate(texts[i]).replace('@',''))
                    TemporaryList1.append('')
            except:
                TemporaryList1.append("Translator had some trouble translating.")
                TemporaryList2.append('')
                TemporaryList2.append(texts[i].replace('@',''))
                TemporaryList1.append('')
        TemporaryList1.append("Video displayed. ")
        TemporaryList2.append('')
        if len(YesNo)>0:
            TemporaryList1.append(interactions[i][0] + ', ' + interactions[i][1] + ', ' + interactions[i][2] + '.')
            TemporaryList2.append('')
    
    
    if 'Hotlink' in media[i]:
        if verified[i]==True:
            TemporaryList1.append("The following from the verified account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        else:
            TemporaryList1.append("The following from account " + usernames[i].replace('@','') + ', ')
            TemporaryList2.append('')
        TemporaryList1.append(weekday + ', ' + datestimes[i][1] + ' at ' + datestimes[i][0] + '. ')
        TemporaryList2.append('')
        TemporaryList1.append("%s posted a link! "%usernames[i].replace('@',''))
        TemporaryList2.append('')
        TemporaryList1.append("%s comment: "%usernames[i].replace('@',''))
        TemporaryList2.append('')
        if languages[i]=='en':
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]=='und':
            TemporaryList1.append("Text blank or undefined!")
            TemporaryList2.append('')
            TemporaryList2.append(texts[i].replace('@',''))
            TemporaryList1.append('')
        if languages[i]!='en' and languages[i]!='und':
            try:
                PreSentence = "Translating from " + langcodes[languages[i]] + "!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            except:
                PreSentence = "Translating from a foreign language!"
                TemporaryList1.append(PreSentence)
                TemporaryList2.append('')
            try:
                t = translate.Translator(from_lang=languages[i],to_lang='en')
                if 'AN INVALID SOURCE LANGUAGE' in t.translate(texts[i]):
                    TemporaryList1.append("Translator had some trouble translating.")
                    TemporaryList2.append('')
                    TemporaryList2.append(texts[i].replace('@',''))
                    TemporaryList1.append('')
                else:
                    TemporaryList2.append(t.translate(texts[i]).replace('@',''))
                    TemporaryList1.append('')
            except:
                TemporaryList1.append("Translator had some trouble translating.")
                TemporaryList2.append('')
                TemporaryList2.append(texts[i].replace('@',''))
                TemporaryList1.append('')
        TemporaryList1.append("Reading link caption and summary. ")
        TemporaryList2.append('')
        t = translate.Translator(from_lang='',to_lang='en')
        if t.translate(headlines[i])=='PLEASE SELECT TWO DISTINCT LANGUAGES' or t.translate(headlines[i])==headlines[i]:
            TemporaryList2.append(headlines[i])
            TemporaryList1.append('')
        elif 'AN INVALID SOURCE LANGUAGE' in t.translate(headlines[i]):
            TemporaryList1.append("Translator had some trouble translating.")
            TemporaryList2.append('')
            TemporaryList2.append(headlines[i])
            TemporaryList1.append('')
        else:
            TemporaryList1.append("Parts had to be translated!")
            TemporaryList2.append('')
            TemporaryList2.append(t.translate(headlines[i]))
            TemporaryList1.append('')
        if t.translate(summaries[i])=='PLEASE SELECT TWO DISTINCT LANGUAGES' or t.translate(summaries[i])==summaries[i]:
            TemporaryList2.append(summaries[i])
            TemporaryList1.append('')
        elif 'AN INVALID SOURCE LANGUAGE' in t.translate(summaries[i]):
            TemporaryList1.append("Translator had some trouble translating.")
            TemporaryList2.append('')
            TemporaryList2.append(summaries[i])
            TemporaryList1.append('')
        else:
            TemporaryList1.append("Parts had to be translated!")
            TemporaryList2.append('')
            TemporaryList2.append(t.translate(summaries[i]))
            TemporaryList1.append('')
        if len(YesNo)>0:
            TemporaryList1.append(interactions[i][0] + ', ' + interactions[i][1] + ', ' + interactions[i][2] + '.')
            TemporaryList2.append('')
    
    
    TweetReaderText1.append(TemporaryList1)
    TweetReaderText2.append(TemporaryList2)

Save = input("\n\nSAVE TEXT FILE? Any key submit = 'YES'; <ENTER> = 'NO'. ")
if len(Save)>0:
    f = open('Twitter_%s-%s.txt'%(timeline,dt.datetime.now().strftime('%m_%d_%y')),'w',errors='ignore')
    f.writelines("THANK YOU FOR USING MICHAEL'S TWEET READER!\n")
    f.writelines("Twitter Account '%s' | %s | "%(timeline,dt.datetime.now().strftime('%m/%d/%y')) + "%s tweets"%len(tweets))
    f.writelines('\n\n')
    for j in range(len(TweetReaderText1)):
        for i in range(len(TweetReaderText1[::-1][j])):
            if TweetReaderText1[::-1][j][i]=='' and TweetReaderText2[::-1][j][i]=='':
                pass
            if TweetReaderText1[::-1][j][i]=='':
                f.writelines(TweetReaderText2[::-1][j][i])
                f.writelines('\n')
            if TweetReaderText2[::-1][j][i]=='':
                f.writelines(TweetReaderText1[::-1][j][i])
                f.writelines('\n')
        f.writelines('\n\n')
    f.close()    

print("Done. \n\n")
ReadNumber = input("How many tweets would you like to read? (There are %s tweets) \n"%len(tweets))

try:
    ReadNumber = int(ReadNumber)
    if ReadNumber > len(tweets):
        input("Invalid input. Will read all %s tweets. Press <ENTER> to continue. \n\n"%len(tweets))
        ReadNumber = len(tweets)
except:
    input("Invalid input, will read half of given tweets. Press <ENTER> continue. \n\n")
    ReadNumber = round(len(tweets)/2)
    

engine1 = tx.init()

vID1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
vID2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
vID3 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"

input("THANK YOU FOR USING MICHAEL'S TWEET READER! PRESS <ENTER> TO PLAY.   ")
for j in range(ReadNumber):
    if j%10==0:
        engine1.setProperty('voice',vID1)
        engine1.setProperty('rate',180)
        engine1.setProperty('volume',0.96)
        engine1.say("Thank you for using Michael's Tweet Reader! You are listening to the Twitter timeline of %s."%timeline)
        engine1.runAndWait()
        s1 = int(dt.datetime.now().strftime('%H'))
        if s1>12:
            s1 = str(s1-12) + dt.datetime.now().strftime(':%M') + ' PM, '
        elif s1==12:
            s1 = str(s1) + dt.datetime.now().strftime(':%M') + ' PM, '
        elif s1==0:
            s1 = str(s1+12) + dt.datetime.now().strftime(':%M') + ' AM, '
        elif 0<s1<12:
            s1 = str(s1) + dt.datetime.now().strftime(':%M') + ' AM, '
        s2 = days[dt.datetime.now().weekday()] + dt.datetime.now().strftime('%h %d %Y')
        engine1.say('It is currently ' + s1 + s2 + '.')
        engine1.runAndWait()
        engine1.say('Now tweet number %s out of %s.' %(j+1,ReadNumber) )
        engine1.runAndWait()
    for i in range(len(TweetReaderText1[::-1][j])):
        if TweetReaderText1[::-1][j][i]=='' and TweetReaderText2[::-1][j][i]=='':
            pass
        if TweetReaderText1[::-1][j][i]=='':
            engine1.setProperty('voice',vID2)
            engine1.setProperty('rate',135)
            engine1.setProperty('volume',0.96)
            engine1.say(TweetReaderText2[::-1][j][i])
            engine1.runAndWait()
        if TweetReaderText2[::-1][j][i]=='':
            engine1.setProperty('voice',vID1)
            engine1.setProperty('rate',200)
            engine1.setProperty('volume',0.96)
            engine1.say(TweetReaderText1[::-1][j][i])
            engine1.runAndWait()

engine1.setProperty('voice',vID1)
engine1.setProperty('rate',170)
engine1.say("This concludes your Tweet reading! Thank you for using Michael's Tweet Reader! ")
engine1.runAndWait()
engine1.setProperty('voice',vID2)
engine1.setProperty('rate',130)
engine1.say("Goodbye! ")
engine1.runAndWait()
input("ALL DONE. This concludes your Tweet reading. Thank you for using Michael's Tweet Reader! \n\n\t Press <ENTER> to Exit. ")