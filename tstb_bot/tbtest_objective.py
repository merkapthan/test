#бот вторая версия
import telebot
from telebot import types
import json
import random
import pyphen
import pymorphy2
import tstb_storage
import tstb_token

class Bot:
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(token)
        self.datastorage=Datastorage()
        #self.keybord_level=0 - потом пригодится
        self.wft={} #waiting_for_text сокращенно

        
        self.bot.message_handler(commands=['start'])(self.start_message)
        self.bot.message_handler(commands=['hi'])(self.hi_message)
        self.bot.message_handler(commands=['sum'])(self.summator)
        self.bot.message_handler(content_types=['text'])(self.send_reaction)
        #self.bot.message_handler(func=lambda message: True)(self.unknown_message) - закоментил потому что конфликтует с предыдущим
        
        print("включили")
    
    def start_message(self, message):
        self.keybord_level=0
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Анекдот')
        itembtn2 = types.KeyboardButton('Погода')
        itembtn3 = types.KeyboardButton('Аналитика от эксперта по всем вопросам')
        itembtn4 = types.KeyboardButton('ссылка на гитхаб пажилова афтара')
        itembtn5 = types.KeyboardButton('Список команд')
        itembtn6 = types.KeyboardButton('Иностранные языки')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
        #if self.keybord_level==0:
        self.bot.send_message(message.chat.id, "Привет ✌️ ", reply_markup=markup)
        self.keybord_level+=1
        #else:
            #self.bot.send_message(message.chat.id, "Вернулись ✌️ ", reply_markup=markup)    
    
    def hi_message(self, message):
        self.bot.reply_to(message, "реплай: привет")
    
    def summator(self, message):
        data = message.text.split()
        digit_data = [int(number) for number in data[1:]]
        result = sum(digit_data)
        self.bot.send_message(message.chat.id, result)
    
    def send_reaction(self, message):
        if message.chat.id in self.wft and self.wft[message.chat.id]: 
            result_text=ForLang.solar_lang(message)
            self.bot.send_message(message.chat.id, result_text)
            self.bot.send_message(message.chat.id, "пока баговано")
            self.wft[message.chat.id]=False
        else:    
            if message.text.lower() == "анекдот":
                joke = random.choice(self.datastorage.jokes)
                self.bot.send_message(message.chat.id, joke)
            elif message.text.lower()=="ссылка на гитхаб пажилова афтара":
                github_link = "<a href='https://github.com/merkapthan'>https://github.com/merkapthan</a>"
                self.bot.send_message(message.chat.id, github_link, parse_mode="HTML")   
            elif message.text.lower() == "погода":
                self.bot.send_message(message.chat.id, "мне впадлу возиться с api погодных сервисов ")
            elif message.text.lower()=="список команд":
                command_dict_str = json.dumps(self.datastorage.command_dict, ensure_ascii=False)
                self.bot.send_message(message.chat.id, command_dict_str)    
            elif message.text.lower()=="иностранные языки":
                self.switch_language(message)    
            elif message.text.lower()=="назад":    
                self.start_message(message)

            elif message.text.lower()=="солнечный":    
                #self.solar_lang(message)
                self.wft[message.chat.id]=True
            elif message.text.lower()=="кирпичный":    
                #self.solar_lang(message)
                self.wft[message.chat.id]=True

            else:
                self.unknown_message(message)    

    def switch_language(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Солнечный')
        itembtn2 = types.KeyboardButton('Кирпичный')        
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        self.bot.send_message(message.chat.id, "Выберите язык:", reply_markup=markup)    


            
    
    def unknown_message(self, message):
        if message.text.startswith("/"):
            if message.text.startswith("/help") or message.text.startswith("список команд"):
                command_dict_str = json.dumps(self.datastorage.command_dict, ensure_ascii=False)
                self.bot.send_message(message.chat.id, command_dict_str)
            else:
                self.bot.send_message(message.chat.id, "незнакомая команда")
        else:
            self.bot.send_message(message.chat.id, message.text)
    
    def run(self):
        self.bot.infinity_polling()
        print("выключили")

class Datastorage:
    def __init__(self):
        self.command_dict = {"/start": "начать", "/hi": "реплай привета", "/sum": "сумма чисел", "/help":"список команд"}
        self.jokes = tstb_storage.jokes

class ForLang:
    @staticmethod
    def solar_lang(message):
        words=message.text.split()
        result_text=[]
        for word in words:
            syllables=ForLang.split_into_syllables(word)
            result_text+=syllables
        return result_text    
          

    @staticmethod
    def split_into_syllables(text): #с помощью pyphen
        dic = pyphen.Pyphen(lang='ru')  # указываем язык (в данном случае русский)
        syllables = dic.inserted(text).split('-')
        return syllables  
    
    
    @staticmethod
    def split_into_syllables_pymorph2(text): #с помощью pymorph2 и видимо оно вообще не работает
        morph = pymorphy2.MorphAnalyzer()
        parsed_word = morph.parse(text)[0]
        syllables = parsed_word[0].word.split('-')
        return syllables
    
    @staticmethod
    def feature_sl_decorator(method_to_decorate): #декоратор, который фиксит неработающий метод solar_lang
        def wrapper(*args, **kwargs):
            # Дополнительная логика перед вызовом метода
            print("Дополнительная логика перед вызовом метода")
            return method_to_decorate(*args, **kwargs)
        return wrapper


bot = Bot(tstb_token.tokenforbot)
bot.run()