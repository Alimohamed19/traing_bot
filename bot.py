from sqlcon import *
import telebot
from info import * 
from telebot.types import ReplyKeyboardMarkup, KeyboardButton , ReplyKeyboardRemove
from Aiinfo import analyze_crypto_data
import json


with open("AiTrading.json", "r", encoding="utf-8") as f:
    ai_trading_message  = json.load(f)

# توكن البوت
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

massg_start = """🎉 Welcome to the Cryptocurrency Bot! 🤖
🪙 This bot helps you track cryptocurrency prices quickly and easily.

👇 Available Commands:
1️⃣ <currency symbol>: Get detailed information about a specific coin (price, daily change, market cap).
📌 Example: BTC

2️⃣ /top_gainers: Check the top gainers in the last 24 hours.
3️⃣ /top_losers: Check the top losers in the last 24 hours.
4️⃣ /AiTrading: You can start using the AI and determine the language to speak

"Hello! We are currently working on developing the interactive chat feature with the bot to provide more accurate and organized cryptocurrency analysis. Users will soon be able to fully interact with the bot to get detailed analysis of cryptocurrencies, market predictions, and the best buy and sell strategies. We are working hard to ensure the best analytical experience for investors. Thank you for your patience, and the feature will be available soon!"

✨ Usage Examples:
BTC ➡️ Get complete details about Bitcoin.
/top_gainers ➡️ See the top-performing coins today.
/top_losers ➡️ See the worst-performing coins today.
💬 If you have any questions or issues, just message me here, and I’ll help you! 😊
    @Botex_botex
"""

# البداية
def welcome(message):
    bot.reply_to(message, f"Hello dear {message.from_user.first_name}")
    bot.send_video(message.chat.id,open("vdios/1.mp4","rb"))
    bot.reply_to(message, massg_start)

# قائمة أعلى العملات صعودًا
def get_top_gainers(message):
    try:
        gainers = get_top_cryptos("gainers")  # دالة مخصصة لجلب أعلى العملات ارتفاعًا
        bot.send_photo(message.chat.id, open("imges/1.jpg", 'rb'))  # إرسال الصورة
        bot.reply_to(message, gainers)  # إرسال النتيجة للمستخدم
    except Exception as e:
        bot.reply_to(message, f"❗️ An error occurred while fetching data for the highest rising currencies: {str(e)}")

# قائمة أعلى العملات هبوطًا
def get_top_losers(message):
    try:
        losers = get_top_cryptos("losers")  # دالة مخصصة لجلب أعلى العملات انخفاضًا
        bot.send_photo(message.chat.id, open("imges/3.jpg", 'rb'))  # إرسال الصورة
        bot.reply_to(message, losers)  # إرسال النتيجة للمستخدم
    except Exception as e:
        bot.reply_to(message, f"❗️ An error occurred while fetching data for the highest declining currencies: {str(e)}")

# معالج /details
def get_details(message):
    try:
        symbol = message.text.upper()
        result = get_crypto_details(symbol)
        if result["image_url"]:
            bot.send_photo(message.chat.id, result["image_url"], caption=result["details"])
        else:
            bot.reply_to(message, result["details"])
    except IndexError:
        bot.reply_to(message, "❗️ Please write the currency symbol. example: BTC")
    except Exception as e:
        bot.reply_to(message, f"❗️ An error occurred: {str(e)}")

# معالج /AiTrading
def ai_trading(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Arabic")
    item2 = KeyboardButton("English")
    item3 = KeyboardButton("Français")
    item4 = KeyboardButton("Russian")
    item5 = KeyboardButton("Chinese")
    markup.add(item1, item2 , item3, item4, item5)
    bot.send_message(message.chat.id, "Welcome to the AI Trading! Please choose your language:", reply_markup=markup)


#/معالج لاختيار اللغة
def choose_language(message):
    armess = ai_trading_message ["ar"]
    enmess = ai_trading_message ["en"]
    fremess = ai_trading_message ["fr"]
    rumess = ai_trading_message ["ru"]
    chmess = ai_trading_message ["ch"]
    if message.text == 'Arabic':
        bot.send_message(message.chat.id, "تم تعيين اللغة إلى العربية.\nالآن يمكنك بدء التحليل والمناقشة حول العملات الرقمية.",reply_markup=ReplyKeyboardRemove())
        #/أرسل تعليمات جديدة باللغة العربية
        bot.send_message(message.chat.id, armess)
        
    elif message.text == 'English':
        bot.send_message(message.chat.id, "Language set to English.\nYou can now start analyzing cryptocurrencies and discussing trading strategies.",reply_markup=ReplyKeyboardRemove())
        # Send new instructions in English
        bot.send_message(message.chat.id, enmess)
    elif message.text == 'Français':
        bot.send_message(message.chat.id, "La langue est définie sur le français.\nVous pouvez maintenant commencer à analyser les crypto-monnaies et à discuter des stratégies de trading.",reply_markup=ReplyKeyboardRemove())
        # Send new instructions in English
        bot.send_message(message.chat.id, fremess)
    elif message.text == 'Russian':
        bot.send_message(message.chat.id, "Язык установлен русский.\nТеперь вы можете начать анализировать криптовалюты и обсуждать торговые стратегии.",reply_markup=ReplyKeyboardRemove())
        # Send new instructions in English
        bot.send_message(message.chat.id, rumess)
    elif message.text == 'Chinese':
        bot.send_message(message.chat.id, "语言设置为中文\n您现在可以开始分析加密货币并讨论交易策略。" , reply_markup=ReplyKeyboardRemove())
        # Send new instructions in English
        bot.send_message(message.chat.id, chmess)
    if user_exists(message.from_user.id):
        update_language(message.from_user.id,message.text)
    else:
        add_user(message.from_user.id,message.text)
    print( get_language(message.from_user.id))  # Assume this retrieves the user's language preference
    


def commqustion(m,example,qustion,time=""):
    try:
        coin = m.text.split()[1].upper()
        time = ""
        print(f"Getting price for: {coin}")
        language = get_language(m.from_user.id)  # Assume this retrieves the user's language preference
        result = analyze_crypto_data(symbol=coin, message=f"{qustion} {coin} {time}?", language=language)
        bot.send_message(m.chat.id, result)
    except IndexError:
        bot.send_message(m.chat.id, f"❗️ Please provide a valid coin name. Example: /{example}")
    except Exception as e:
        bot.send_message(m.chat.id, f"❗️ An error occurred: {e}")
        
def cmmqustionall(m,qustion):
    try:
        language = get_language(m.from_user.id)
        result = analyze_crypto_data(symbol="BTC", message=qustion, language=language)
        bot.send_message(m.chat.id,result)
    except Exception as e:
        bot.send_message(m.chat.id, f"❗️ An error occurred: {e}")

# معالج الأوامر العامة
@bot.message_handler(func=lambda m: True)
def rm(m):
    if m.text == '/start':
        welcome(m)
    elif m.text == '/top_gainers':
        get_top_gainers(m)
    elif m.text == '/top_losers':
        get_top_losers(m)
    elif m.text == '/AiTrading':
        ai_trading(m)
    elif m.text == 'Arabic' or m.text == 'English' or m.text == 'Français' or m.text == 'Russian' or m.text == 'Chinese':
        choose_language(m)
    elif m.text.split()[0] == '/price':
        commqustion(m,"price BTC" , "What is the current price of" ,"naw")
    elif m.text.split()[0] == '/change':
        time = m.text.split()[2] if len(m.text.split()) > 2 else "day"
        commqustion(m,"change BTC day/wek/month","Describe the change that occurred in",time=f"during the {time}")
    elif m.text.split()[0] == '/reasons':
        commqustion(m,"reasons BTC","What are the reasons that led to the price of a currency changing",time="In the recent period")
    elif m.text.split()[0] == '/comparison':
        commqustion(m,"comparison BTC","Is it a currency price",time="Relative to history")
    elif m.text.split()[0] == '/upcoming_events':
        commqustion(m,"upcoming_events BTC","Inform me of upcoming events that may affect the price")
    elif m.text.split()[0] == '/target_price':
        commqustion(m,"target_price BTC","That is, the expected or target price of a currency",time="In the next period of time")
    elif m.text.split()[0] == '/monitor':
        commqustion(m,"monitor BTC","How to monitor price",time="Observantly")
    elif m.text.split()[0] == '/analysis':
        commqustion(m,"analysis BTC","Give me analytics that indicate that price")
    elif m.text.split()[0] == '/technical_analysis':
        commqustion(m,"technical_analysis BTC","How to apply technical analysis to digital currencies")
    elif m.text.split()[0] == '/trend':
        commqustion(m,"trend BTC","Use technical analysis to predict price trends")
    elif m.text.split()[0] == '/indicators':
        commqustion(m,"indicators BTC","Know the most useful technical indicators for price analysis")
    elif m.text.split()[0] == '/buy_sell_signals':
        commqustion(m,"buy_sell_signals BTC","Define signals to buy or sell a currency" ,time="On Japanese cartoons")
    elif m.text.split()[0] == '/ma':
        commqustion(m,"ma BTC","How to use moving averages for a currency" ,time="To predict its price movement")
    elif m.text.split()[0] == '/rsi':
        commqustion(m,"rsi BTC","How to use the RSI for a currency" ,time="To analyze its movement")
    elif m.text.split()[0] == '/support_resistance':
        commqustion(m,"support_resistance BTC","What are the support and resistance points for a currency")
    else:
        get_details(m)
    
    username = m.from_user.username if m.from_user.username else "No username"
    print(f"message: {m.text} name: {m.from_user.first_name} {m.from_user.last_name} username: {username} id: {m.from_user.id}")
    
# بدء البوت
bot.infinity_polling()