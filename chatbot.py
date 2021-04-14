from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bs4 import BeautifulSoup
import os
import logging
import json
import requests
import time
import random



def main():
    # Load your token and create an Updater for your Bot

    config = {
        "TELEGRAM":{
            "ACCESS_TOKEN":os.environ["tg_token"]
        }
    }

    updater = Updater(
        token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", echo))
    dispatcher.add_handler(CommandHandler("covid19", covidtips))
    dispatcher.add_handler(CommandHandler("lwtips", lwtips))
    dispatcher.add_handler(CommandHandler("hdtips", hdtips))
    dispatcher.add_handler(CommandHandler("cal", callthecal))
    dispatcher.add_handler(CommandHandler("calories", calories))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = "Welcome to Health Genius!\r\n"
    reply_message+=genHKCovidSummary()
    reply_message+="\r\n\r\n"
    reply_message+="You can use the following command to use this robot:\r\n"
    reply_message+="/covid19 Provide Hong Kong COVID19 epidemic situation and prevention tips.\r\n"
    reply_message+="/lwtips Give you a weight loss tip\r\n"
    reply_message+="/hdtips Give you a tip about healthy dietary.\r\n"
    reply_message+="/cal Start the Health Genius calculator to calculate your BMI, BMR and REE index.\r\n"
    reply_message+="/calories Query the calories of food. Usage: /calories <keyword>\r\nExample: /calories hamburger\r\n"
    reply_message+="/help Show command description."


    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


def covidtips(update: Update, context: CallbackContext) -> None:
    reply=genHKCovidSummary()
    reply+="\r\n7 Ways to Fight the Virus under the New Normal:"
    reply+="""
Wear a mask
The wearing of mask in all public places (indoor or outdoor) is mandated (unless exempted under Cap. 599I). It is important to wear a mask properly, including performing hand hygiene before wearing and after removing a mask.

Practise hand hygiene
Perform hand hygiene frequently, especially before touching the mouth, nose or eyes, after touching public installations such as handrails or doorknobs, or when hands are contaminated by respiratory secretions after coughing or sneezing.
Wash hands with liquid soap and water, and rub for at least 20 seconds. Then rinse with water and dry with a disposable paper towel or a clean towel. If hand washing facilities are not available, or when hands are not visibly soiled, performing hand hygiene with 70 to 80 per cent alcohol-based handrub is an effective alternative.

Maintain social distancing
Members of the public are advised strongly to reduce social contact to protect themselves and others: Maintain social distance, keep a distance of at least 1 metre from others. Minimise gatherings and trips outside home. Minimise meal gatherings. Use serving utensils. Avoid crowded places.

Seek early medical consultation
Members of the public are advised to seek medical advice promptly when feeling unwell (even if having very mild symptoms only). The Department of Health provides free testing of COVID-19 for private doctors. General outpatient clinics also continue distribution of specimen packs without the need to see doctors.

Protect the elderly
The Government strongly urges the elderly to stay home as far as possible and avoid going out. They should consider asking their family and friends to help with everyday tasks such as shopping for basic necessities.

Keep a diary
To assist contact tracing, keep a diary of your schedule, for example, write down the taxi license plate number you take.
You may also use the “LeaveHomeSafe” mobile app to keep your visit records.

Join COVID-19 testing
Join COVID-19 testing service for the public and targeted groups.
Source:Centre for Health Protection,Hong Kong SAR\r\n
    """

    update.message.reply_text(reply)

def hdtips(update: Update, context: CallbackContext) -> None:
    tList=[
        "Prepare most of your meals at home using whole or minimally processed foods. Choose from a variety of different proteins to keep things interesting. Using catchy names for each day can help you plan.",
        "Make an eating plan each week – this is the key to fast, easy meal preparation. ",
        "Choose recipes with plenty of vegetables and fruit. Your goal is to fill half your plate with vegetables and fruit at every meal. Choose brightly coloured fruits and vegetables each day, especially orange and dark green vegetables.Frozen or canned unsweetened fruits and vegetables are a perfect alternative to fresh produce.",
        "Avoid sugary drinks and instead drink water. Lower-fat, unsweetened milk is also a good way to stay hydrated. Keep a reusable water bottle in your purse or car so you can fill up wherever you are going.",
        "Eat smaller meals more often. Eat at least three meals a day with snacks in between. When you wait too long to eat you are more likely to make unhealthy food choices. Keep easy-to-eat snacks in your purse or bag for emergencies.",
    ]
    i=random.randint(0,len(tList)-1)
    reply="A tip about healthy dietary:\r\n"
    reply+=tList[i]
    reply+="\r\n\r\nSource:Heart and Stroke Foundation of Canada\r\n"
    reply+="If you want to know more, you can enter /hdtips again"

    update.message.reply_text(reply)

def lwtips(update: Update, context: CallbackContext) -> None:
    tList=[
        "Do not skip breakfast\r\nSkipping breakfast will not help you lose weight. You could miss out on essential nutrients and you may end up snacking more throughout the day because you feel hungry.",
        "Eat regular meals\r\nEating at regular times during the day helps burn calories at a faster rate. It also reduces the temptation to snack on foods high in fat and sugar.",
        "Eat plenty of fruit and veg\r\nFruit and veg are low in calories and fat, and high in fibre – 3 essential ingredients for successful weight loss. They also contain plenty of vitamins and minerals.",
        "Get more active\r\nBeing active is key to losing weight and keeping it off. As well as providing lots of health benefits, exercise can help burn off the excess calories you cannot lose through diet alone.",
        "Drink plenty of water\r\nPeople sometimes confuse thirst with hunger. You can end up consuming extra calories when a glass of water is really what you need.",
        "Eat high fibre foods\r\nFoods containing lots of fibre can help keep you feeling full, which is perfect for losing weight. Fibre is only found in food from plants, such as fruit and veg, oats, wholegrain bread, brown rice and pasta, and beans, peas and lentils.",
        "Read food labels\r\nKnowing how to read food labels can help you choose healthier options. Use the calorie information to work out how a particular food fits into your daily calorie allowance on the weight loss plan.",
        "Use a smaller plate\r\nUsing smaller plates can help you eat smaller portions. By using smaller plates and bowls, you may be able to gradually get used to eating smaller portions without going hungry. It takes about 20 minutes for the stomach to tell the brain it's full, so eat slowly and stop eating before you feel full.",
        "Do not ban foods\r\nDo not ban any foods from your weight loss plan, especially the ones you like. Banning foods will only make you crave them more. There's no reason you cannot enjoy the occasional treat as long as you stay within your daily calorie allowance.",
        "Do not stock junk food\r\nTo avoid temptation, do not stock junk food – such as chocolate, biscuits, crisps and sweet fizzy drinks – at home. Instead, opt for healthy snacks, such as fruit, unsalted rice cakes, oat cakes, unsalted or unsweetened popcorn, and fruit juice.",
        "Cut down on alcohol\r\nA standard glass of wine can contain as many calories as a piece of chocolate. Over time, drinking too much can easily contribute to weight gain.",
        "Plan your meals\r\nTry to plan your breakfast, lunch, dinner and snacks for the week, making sure you stick to your calorie allowance. You may find it helpful to make a weekly shopping list."
    ]
    i=random.randint(0,len(tList)-1)
    reply="A tip to help you lose weight:\r\n"
    reply+=tList[i]
    reply+="\r\n\r\nSource:National Health Service,the UK\r\n"
    reply+="If you want to know more, you can enter /lwtips again"

    update.message.reply_text(reply)

def callthecal(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Click the link below to enter the calculator:\r\nhttp://45.77.40.34')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    reply_message=""
    reply_message+="You can use the following command to use this robot:\r\n"
    reply_message+="/covid19 Provide Hong Kong COVID19 epidemic situation and prevention tips.\r\n"
    reply_message+="/lwtips Give you a weight loss tip\r\n"
    reply_message+="/hdtips Give you a tip about healthy dietary.\r\n"
    reply_message+="/cal Start the Health Genius calculator to calculate your BMI, BMR and REE index.\r\n"
    reply_message+="/calories Query the calories of food. Usage: /calories <keyword>\r\nExample: /calories hamburger\r\n"
    reply_message+="/help Show command description."
    update.message.reply_text(reply_message)



def calories(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        logging.info(context.args[0])
        # /add keyword <-- this should store the keyword
        msg = context.args[0]
        if msg.strip() =="":
            update.message.reply_text('Usage: /calories <keyword>\r\nExample: /calories hamburger')
        else:
            info="The following are the calories of foods related to \"%s\":\r\nSource:National Health Service,the UK & Nutracheck App"%(msg)
            update.message.reply_text(info)
            for line in getCalorieInfo(msg):
                update.message.reply_text(line)
            update.message.reply_text("=====End=====")
            

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /calories <keyword>')



def getContent(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    try:
        content = requests.get(url, headers=headers).text
        return content
    except Exception as e:
        print("Error occured Url:%s" % (url))
        print(e)
        return False

def genHKCovidSummary():
    nowTimeStamp=int(round(time.time())*1000)
    keyNumApiUrl="https://chp-dashboard.geodata.gov.hk/covid-19/data/keynum.json?_="+str(nowTimeStamp)
    jsonObj=json.loads(getContent(keyNumApiUrl))
    summary="Up to now, the statistics of the COVID-19 epidemic in Hong Kong:\r\n"
    summary+="Confirmed:"+str(jsonObj["Confirmed"])+"\r\n"
    summary+="Hospitalised:"+str(jsonObj["Hospitalised"])+"\r\n"
    summary+="Discharged:"+str(jsonObj["Discharged"])+"\r\n"
    summary+="Critical:"+str(jsonObj["Critical"])+"\r\n"
    summary+="Death:"+str(jsonObj["Death"])+"\r\n"
    summary+="Source:Centre for Health Protection,Hong Kong SAR\r\n"

    return summary

def getCalorieInfo(kw):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    jsonObj=json.loads(requests.post("https://preview.antbits.com/choices_production/calorie_checker/proxy.php",headers=headers,data={"val":kw}).text)
    
    infoList=[]
    for line in jsonObj["results"]["products"]:
        infoLine=""
        infoLine+="Description:"+line["description"]+"\r\n"
        infoLine+="Size/Unit:"+line["servings"]["serving"]["name"]+"\r\n"
        infoLine+="KCal:"+line["servings"]["serving"]["kcal"]+"\r\n"
        infoLine+="Fat(g):"+line["servings"]["serving"]["fatg"]
        infoList.append(infoLine)

    return(infoList)


if __name__ == '__main__':
    main()
