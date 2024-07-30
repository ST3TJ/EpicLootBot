# TODO Fix players saving

import os
import random
import json
import requests
from dotenv import load_dotenv
from telebot import TeleBot, types
from typing import Dict, Optional, Any

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
USER_DATA_FILE = 'users.json'

bot = TeleBot(API_TOKEN)

bot.set_my_commands([
    types.BotCommand('/start', 'Начать игру'),
    types.BotCommand('/get_item', 'Получить новый предмет'),
    types.BotCommand('/stats', 'Посмотреть свои характеристики')
])

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

class Player:
    def __init__(self):
        self.Stats = Stats()
        self.level = 0
        self.exp = 0
        self.last_get = 0


def load_players() -> Dict[str, Any]:
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}


def save_players() -> None:
    return NotImplemented
    # with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
    #     json.dump(players, file, ensure_ascii=False, indent=4)


def get_current_unix_time() -> Optional[int]:
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
        response.raise_for_status()
        return response.json()['unixtime']
    except requests.RequestException as e:
        print(f'Error fetching time: {e}')
        return None


items = [
    Item('Хуй тебе в рот', 0, 0, 0, 1),
    Item('Обыкновенный Магический меч', 10, 0, 0, 0.5),
    Item('Редкие Ловкие сапоги', 0, 10, 0, 0.3),
    Item('Легендарная Мудрая книга', 0, 0, 10, 0.2),
]

players = load_players()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Player()
        save_players()
    bot.reply_to(message, 'Добро пожаловать в EpicLootBot! Используйте команду /get_item для получения случайного предмета.')


@bot.message_handler(commands=['get_item'])
def get_item(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Player()
    
    item = random.choices(items, weights=[item.chance for item in items], k=1)[0]
    players[user_id].Stats.strength += item.stats.strength
    players[user_id].Stats.agility += item.stats.agility
    players[user_id].Stats.intelligence += item.stats.intelligence
    
    response = f"Вы получили: {item.name} (+{item.stats.strength} к силе, +{item.stats.agility} к ловкости, +{item.stats.intelligence} к интеллекту)."
    bot.reply_to(message, response)
    save_players()


@bot.message_handler(commands=['stats'])
def show_stats(message):
    user_id = message.from_user.id
    if user_id not in players:
        players[user_id] = Player()
        save_players()
    
    stats = players[user_id]
    response = f"Ваши характеристики:\nСила: {stats.strength}\nЛовкость: {stats.agility}\nИнтеллект: {stats.intelligence}"
    bot.reply_to(message, response)


bot.polling(non_stop=True, interval=0)