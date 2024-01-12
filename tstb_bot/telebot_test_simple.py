#telebot_test
import telebot
from telebot import types
import json
import random

token="6953039131:AAFpgE7PQVUTtZmXUrphWR16s3g9ZvAJesw"
command_dict={"/start":"начать", "/hi":"реплай привета", "sum":"сумма чисел"}
jokes = ["Нажимаю мой компьютер, а он не моет"]


bot=telebot.TeleBot(token)
print ("включили")

@bot.message_handler(commands=['start'])
def start_message(message):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  itembtn1 = types.KeyboardButton('Анекдот')
  itembtn2 = types.KeyboardButton('Погода')
  itembtn3 = types.KeyboardButton('Аналитика от эксперта по всем вопросам')
  itembtn4 = types.KeyboardButton('ссылка на гитхаб пажилова афтара')
  markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
  bot.send_message(message.chat.id,"Привет ✌️ ", reply_markup=markup)

@bot.message_handler(commands=['hi'])
def hi_message(message):
  bot.reply_to(message,"реплай: привет") 
 
@bot.message_handler(commands=['sum'])   
def summator(message):
  data=message.text.split()
  digit_data=[int(sum) for number in data [1:]]
  result=sum(digit_data)
  bot.send_message(message.chat.id, result)


@bot.message_handler(content_types=['text'])
def send_reaction(message):
    if message.text=="Анекдот":
      joke = random.choice(jokes)
      bot.send_message(message.chat.id, joke)
    elif message.text=="Погода":
      bot.send_message(message.chat.id, "Холодно очень холодно, палочки да кружочки")  

@bot.message_handler(func=lambda message:True)
def unknown_message(message):
  if message.text.startswith("/"):
    if message.text.startswith("/help") or message.text.startswith("список команд"):
      command_dict_str=json.dumps(command_dict, ensure_ascii=False) #если не прописать еншуреассии то собьется кодировка
      bot.send_message(message.chat.id, command_dict_str)
    else:  
      bot.send_message(message.chat.id, "незнакомая команда")
  else:
   bot.send_message(message.chat.id, message.text)         
   
bot.infinity_polling()
print("выключили") #бесконечное прослушивание 
#bot.polling()
