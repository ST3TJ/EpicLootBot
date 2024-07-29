import os
import random
from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

bot = TeleBot(API_TOKEN)

bot.set_my_commands([
    types.BotCommand('/start', 'Начать игру'),
    types.BotCommand('/get_item', 'Получить новый предмет'),
    types.BotCommand('/stats', 'Посмотреть свои характеристики')
])

players = {}

class Stats:
    def __init__(self, strength: float = 0, agility: float = 0, intelligence: float = 0):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

class Item:
    def __init__(self, name: str, strength: float, agility: float, intelligence: float, chance: float):
        self.name = name
        self.stats = Stats(strength, agility, intelligence)
        self.chance = chance

items = [
    Item('Магический меч', 10, 0, 0, 0.5),
    Item('Ловкие сапоги', 0, 10, 0, 0.3),
    Item('Мудрая книга', 0, 0, 10, 0.2),
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Stats()
    bot.reply_to(message, 'Добро пожаловать в EpicLootBot! Используйте команду /get_item для получения случайного предмета.')

@bot.message_handler(commands=['get_item'])
def get_item(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Stats()
    
    item = random.choices(items, weights=[item.chance for item in items], k=1)[0]
    players[user_id].strength += item.stats.strength
    players[user_id].agility += item.stats.agility
    players[user_id].intelligence += item.stats.intelligence
    
    response = f"Вы получили: {item.name} (+{item.stats.strength} к силе, +{item.stats.agility} к ловкости, +{item.stats.intelligence} к интеллекту)."
    bot.reply_to(message, response)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Stats()
    
    stats = players[user_id]
    response = f"Ваши характеристики:\nСила: {stats.strength}\nЛовкость: {stats.agility}\nИнтеллект: {stats.intelligence}"
    bot.reply_to(message, response)

bot.polling(non_stop=True, interval=0)