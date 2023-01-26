import telebot
from telebot import TeleBot
from telebot import types
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# ---> .env file <----
#bot API
API = os.getenv('API_KEY')
#admin tg-ID
Admin_telegram_ID = os.getenv('Admin_telegram_ID')

bot = telebot.TeleBot(API)

welcome_message = """
የልቤ ጌታ Album V1
"""

bot_info = """
ከታች በተዘረዘሩት የባንክ አማራጮች 100 ብር በመክፈል የልቤ ጌታ አልበምን ያግኙ።
ብርሀን ባንክ
100078733905
ዳሸን ባንክ
5044102309011
ንግድ ባንክ
1000353787164 
ንብ ባንክ
7000017256861
አዋሽ ባንክ
01347521716200253
"""
bot_help = """
-------HELP-------
available commands
/start 
/Help
/Buy_albums
/Info
/GetAccountNumber
/buy

"""
accounts = """
ብርሀን ባንክ
100078733905
ዳሸን ባንክ
5044102309011
ንግድ ባንክ
1000353787164 
ንብ ባንክ
7000017256861
አዋሽ ባንክ
01347521716200253 
"""

try:

  print(welcome_message)
  #send  information to telegram user;
  def send_message_to_telegram(msg):
      chatID = Admin_telegram_ID
      apiURL = f'https://api.telegram.org/bot{API}/sendMessage'
      try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': msg})
        print(response.text)
      except Exception as e:
          print(e)

  @bot.message_handler(commands=['start'])
  def start(message):
    #url of welcome image [image link]
    url = "https://thumbs.dreamstime.com/b/stick-figures-holding-word-welcome-vector-banner-text-welcome-welcome-together-people-big-colorful-letters-114865217.jpg"
    bot.send_photo(
      message.chat.id,
      photo=url
    )
    markup = types.ReplyKeyboardMarkup()
    start_btn = types.KeyboardButton('/start')
    buyAlbum_btn = types.KeyboardButton('/Buy_Albums')
    info_btn = types.KeyboardButton('/Info')
    help_btn = types.KeyboardButton('/Help')

    markup.row(start_btn)
    markup.row(info_btn, help_btn)
    markup.row(buyAlbum_btn)
    bot.send_message(message.chat.id, "የልቤ ጌታ Album Telegram Bot", reply_markup=markup)


  @bot.message_handler(commands=['Buy_Albums'])
  def info(message):
    markup = types.ReplyKeyboardMarkup()
    bank_btn = types.KeyboardButton('/GetAccountNumber')
    buy_btn = types.KeyboardButton('/buy')
    markup.row(bank_btn)
    markup.row(buy_btn)
    
    bot.send_message(message.chat.id, "Payment Options", reply_markup=markup)
    @bot.message_handler(commands=['GetAccountNumber'])
    def info(message):
      bot.reply_to(message, accounts)

    def recive_photo_and_send():
      bot.send_message(message.chat.id, "Send payment screenshot")
      @bot.message_handler(content_types=['photo'])
      def photo(message):
        # print('message.photo =', message.photo)
        fileID = message.photo[-1].file_id
        # print('fileID =', fileID)
        file_info = bot.get_file(fileID)
        # print('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        # send_image_to_telegram(path)
        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_photo(chat_id=Admin_telegram_ID, photo=open('image.jpg', 'rb'))
        bot.send_message(chat_id=Admin_telegram_ID, text="******************************")
        bot.reply_to(message, "image recieved..")
        bot.send_message("Please wait for admin's response...")

    @bot.message_handler(commands=['buy'])
    def sendDataToAdmin(message):
      bot.send_message(message.chat.id, "1. Enter your name, 2. telegram username 3. phone number")
      @bot.message_handler(func=lambda message: True)
      def echo_all(message):
        info = message.text
        bot.send_message(chat_id=Admin_telegram_ID, text="******************************")
        send_message_to_telegram(info)
        bot.reply_to(message, "information recorded")
        recive_photo_and_send()
        
  @bot.message_handler(commands=['Info'])
  def info(message):
    bot.send_message(message.chat.id, bot_info)
    
  @bot.message_handler(commands=['Help'])
  def info(message):
    bot.send_message(message.chat.id, bot_help)
      
  bot.polling()
except Exception as e:
          print(e)
