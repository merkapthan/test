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
        self.wfl={} #waiting_for_language

        
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
            result_text=ForLang.translate(message, self.wfl[message.chat.id])
            self.bot.send_message(message.chat.id, result_text)
            #self.bot.send_message(message.chat.id, "пока баговано")
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
            elif message.text.lower() == "аналитика от эксперта по всем вопросам":
                self.bot.send_message(message.chat.id, "мне впадлу возиться с этим пока ")
            elif message.text.lower()=="список команд":
                command_dict_str = json.dumps(self.datastorage.command_dict, ensure_ascii=False)
                self.bot.send_message(message.chat.id, command_dict_str)    
            elif message.text.lower()=="иностранные языки":
                self.switch_language(message)    
            elif message.text.lower()=="назад":    
                self.start_message(message)

            elif message.text.lower()=="солнечный":
                self.bot.send_message(message.chat.id, "напишите фразу для перевода")   
                #self.solar_lang(message)
                self.wft[message.chat.id]=True
                self.wfl[message.chat.id]="sol"
            elif message.text.lower()=="кирпичный": 
                self.bot.send_message(message.chat.id, "напишите фразу для перевода")      
                #self.solar_lang(message)
                self.wft[message.chat.id]=True
                self.wfl[message.chat.id]="brick"

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
        self.vowels = {"eng":"aeiou", "rus":"аеёиоуыэюя"}
        self.consonants =  {"eng":"bcdfghjklmnpqrstvwxyz", "rus":"бвгджзйклмнпрстфхцчшщ"}

class ForLang:
    @staticmethod #метод, ставящий пробелы между буквами
    def add_spaces(text):
        spaced_text = ""
        for char in text:
            if char.isalpha():
                spaced_text += char + " "
            elif char.isspace():
                spaced_text += char * 2
        return spaced_text
    
    @staticmethod #метод, удаляющий слог (слоги) из предложения
    def remove_syllables(sentence, syllable):
        #for syllable in syllables:
        sentence = sentence.replace(syllable, "")
        return sentence
    
    @staticmethod
    def sentence_to_list(sentence): #метод, делающий список из слов в предложении
        words_list = sentence.split()
        return words_list
    
    @staticmethod
    def insert_s_after_vowels(word): #метод переводит отдельные слова на солнечный   
        new_word=""
        for char in word:
            new_word+=char
            if char.lower() in bot.datastorage.vowels["rus"]:
                new_word+="с"+char.lower()
            elif char.lower() in bot.datastorage.vowels["eng"]:
                new_word+="s"+char.lower()    

        return new_word
    
    @staticmethod
    def insert_p_before_syllables(word): #метод переводит отдельные слова на кирпичный  
        new_word="" 
        new_syl=""      
        to_add="" 
        for char in word:            
            new_syl+=char
            to_add+=char
            if char.lower() in bot.datastorage.vowels["rus"]:
                new_syl="п"+char.lower()+new_syl
                new_word+=new_syl
                new_syl="" 
                to_add=""
                #break
            elif char.lower() in bot.datastorage.vowels["eng"]:
                new_syl="p"+char.lower()+new_syl
                new_word+=new_syl
                new_syl="" 
                to_add=""
                #break
            #new_word+=new_syl   
        #for i in range(len(list(word))):             
            #if list(word)[-i-1] in bot.datastorage.vowels:
               # break
           # to_add+=str(list(word)[-i-1])
        #new_word+=to_add[::-1]  
        new_word+=to_add      
        return new_word

    @staticmethod
    def translate(message, lang):
        text=message.text
        words_list=ForLang.sentence_to_list(text)
        new_words_list=[]
        for word in words_list:
            if lang=="sol":
                new_word=ForLang.insert_s_after_vowels(word)
            elif lang=="brick":
                new_word=ForLang.insert_p_before_syllables(word)
            new_words_list.append(new_word)
        new_text=" ".join(new_words_list)
        return new_text.capitalize()



bot = Bot(tstb_token.tokenforbot)
bot.run()