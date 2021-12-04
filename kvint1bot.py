from transitions import Machine
import telebot
from telebot import types
bot = telebot.TeleBot('2112103382:AAG5xWnUnhr7AeZOFcWtab7ARrwiCVlcHeQ')
class customer(object):
    states=['dumbass','bigpizza','smallpizza','regbc','regbb','regsc','regsb','ex']
    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=customer.states, initial='dumbass')
        self.machine.add_transition('big','dumbass','bigpizza')
        self.machine.add_transition('small','dumbass','smallpizza')
        self.machine.add_transition('cash','bigpizza','regbc')
        self.machine.add_transition('bank','bigpizza','regbb')
        self.machine.add_transition('cash','smallpizza','regsc')
        self.machine.add_transition('bank','smallpizza','regsb')
        self.machine.add_transition('yes','*','ex')
        self.machine.add_transition('reset','*','dumbass')
botstate=customer("DUMB")

@bot.message_handler(commands=["start"])
def start(m, res=False):
    botstate.reset()
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Большую")
    item2=types.KeyboardButton("Маленькую")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, 'Какую вы хотите пиццу? Большую или маленькую?',reply_markup=markup)
    bot.register_next_step_handler(m, handle_text_bs)

@bot.message_handler(content_types=["text"])
def handle_text_bs(message):
    markup=types.ReplyKeyboardRemove()
    if message.text.strip().lower() == 'большую':
        botstate.big()
    if message.text.strip().lower()  == 'маленькую' :
        botstate.small()
    print (botstate.state)
    markup2=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item3=types.KeyboardButton("Наличкой")
    item4=types.KeyboardButton("Безналом")
    markup2.add(item3)
    markup2.add(item4)
    bot.send_message(message.chat.id, 'Как вы будете платить?',reply_markup=markup2)
    bot.register_next_step_handler(message, hanle_text_cb)

def hanle_text_cb(message):
    markup2=types.ReplyKeyboardRemove()
    markup3=types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text.strip().lower() == 'наличкой' :
        botstate.cash()
    if message.text.strip().lower() == 'безналом' :
        botstate.bank()
    print (botstate.state)
    item5=types.KeyboardButton("Да")
    item6=types.KeyboardButton("Нет")
    markup3.add(item5)
    markup3.add(item6)
    if botstate.state == 'regbc':
        state='Вы хотите большую пиццу, оплата наличкой?'
    if botstate.state == 'regbb':
        state='Вы хотите большую пиццу, оплата картой?'
    if botstate.state == 'regsc':
        state='Вы хотите маленькую пиццу, оплата наличкой?'
    if botstate.state == 'regsb':
        state='Вы хотите маленькую пиццу, оплата картой?'
    bot.send_message(message.chat.id, state ,reply_markup=markup3) 
    bot.register_next_step_handler(message, handle_text_yn)

def handle_text_yn(message):
    markup3=types.ReplyKeyboardRemove()
    markup4=types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text.strip().lower() == 'да' :
        markup4=types.ReplyKeyboardRemove()
        botstate.yes()
        bot.send_message(message.chat.id, 'Спасибо за заказ!',reply_markup=markup4)
    if message.text.strip().lower() == 'нет' :
        start(message)

bot.polling(none_stop=True, interval=0)
