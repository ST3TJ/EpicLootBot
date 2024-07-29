import os
import telebot
import random

API_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(API_TOKEN)    

players = {}

items = [
    {"name": "Магический меч", "strength": 10, "agility": 0, "intelligence": 0},
    {"name": "Ловкие сапоги", "strength": 0, "agility": 10, "intelligence": 0},
    {"name": "Мудрая книга", "strength": 0, "agility": 0, "intelligence": 10},
]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = {"strength": 0, "agility": 0, "intelligence": 0}
    bot.reply_to(message, "Добро пожаловать в FantasyQuestBot! Используйте команду /get_item для получения случайного предмета.")


@bot.message_handler(commands=['get_item'])
def get_item(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = {"strength": 0, "agility": 0, "intelligence": 0}
    
    item = random.choice(items)
    players[user_id]["strength"] += item["strength"]
    players[user_id]["agility"] += item["agility"]
    players[user_id]["intelligence"] += item["intelligence"]
    
    response = f"Вы получили: {item['name']} (+{item['strength']} к силе, +{item['agility']} к ловкости, +{item['intelligence']} к интеллекту)."
    bot.reply_to(message, response)



@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = {"strength": 0, "agility": 0, "intelligence": 0}
    
    stats = players[user_id]
    response = f"Ваши характеристики:\nСила: {stats['strength']}\nЛовкость: {stats['agility']}\nИнтеллект: {stats['intelligence']}"
    bot.reply_to(message, response)


bot.polling()