import os
import time
import random
import requests
from dotenv import load_dotenv

def send_to_TG(text, chat_id = None, bot_token = None):
    url = f"https://api.telegram.org/{bot_token}/sendMessage"
    params = {
    'chat_id': chat_id,
    'text': text,
    'parse_mode':"html"
    }
    try: response = requests.post(url, verify=True, params=params)
    except Exception: print (Exception)
    try:
        if response.status_code != 200:(
            print (text))
    except Exception: print (Exception)

def buy_best_upgrade():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Android 12; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://hamsterkombat.io/',
        'Authorization': authorization,
        'Origin': 'https://hamsterkombat.io',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
    }

    try: response = requests.post('https://api.hamsterkombatgame.io/clicker/upgrades-for-buy', headers=headers).json()
    except Exception as e: send_to_TG(e, chat_id = chat_id, bot_token = bot_token)
    upgrades = [
        item for item in response["upgradesForBuy"]
        if not item["isExpired"] and item["isAvailable"] and item["price"] > 0
    ]

    toppest_upgrades = [["", int(0), "0"]]
    for i in upgrades:
        try:
            id = i["id"]
            efficiency_coeff = i["profitPerHour"] / i["price"]
            price = i["price"]
        except Exception as e:
            print(f"Sth happens wrong in checking:\n'{i}'")
            print(e)
        try:
            if efficiency_coeff > 0.003:
                top_up = [id, efficiency_coeff, price]
                toppest_upgrades.append(top_up)
        except Exception as e:
            print(f"Sth happens wrong in adding to list:\n'{i}'")
            print(e)
    formatted_date = time.strftime("%d.%m.%Y %H:%M", time. localtime())
    toppest_upgrades.pop(0)
    print (toppest_upgrades)
    sorted_upgrades = sorted(toppest_upgrades, key=lambda x: x[1])
    print (sorted_upgrades)
    for up in sorted_upgrades:
        upgrade_id = up[0]
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization,
            "Origin": "https://hamsterkombat.io",
            "Referer": "https://hamsterkombat.io/"
        }
        data = {
            "upgradeId": upgrade_id,
            "timestamp": int(time.time() * 1000)
        }
        try:
            response = requests.post("https://api.hamsterkombatgame.io/clicker/buy-upgrade",
                                     headers=headers, json=data)
        except Exception as e:
            send_to_TG(e, chat_id=chat_id,
                        bot_token=bot_token)
        if response and response.status_code == 200:
            formatted_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
            price = f"{up[2]:,}".replace(",", "'")
            text = f"[{formatted_date}]\nUpgrade {up[0]} is purcashed.\nPrice - <b>{price}</b>"
            send_to_TG(text, chat_id=chat_id,
                        bot_token=bot_token)
#               if response.status_code == 400:
#                  print(f"Upgrade {up[0]} cannot be percashed. Price {up[2]}")

def get_avaliable_taps():
    # Получаем количество доступных тапов
    try: response = requests.post(
        'https://api.hamsterkombatgame.io/clicker/sync',
        headers={
            'Content-Type': 'application/json',
            'Authorization': authorization
        },
        json={}
    )
    except Exception as e: send_to_TG(e, chat_id = chat_id, bot_token = bot_token)
    try: taps = response.json().get('clickerUser', {}).get('availableTaps', 0)
    except Exception as e:
        send_to_TG(e, chat_id = chat_id, bot_token = bot_token)
        taps = 14
    return taps

# загрузка из переменных окружения
load_dotenv()
chat_id = os.getenv("chat_id")
bot_token = os.getenv("bot_token")
authorization = os.getenv("authorization")
# В моем случае предел равен 7000
try: load_capacity =  os.getenv("capacity")
except: load_capacity = None
capacity = int(load_capacity)-2000 if load_capacity else 900

while True:
    # Получаем количество доступных тапов
    taps = get_avaliable_taps()
    count = int(random.uniform(0, taps))

    time.sleep(1)

    # Отправляем запрос для выполнения тапов
    try:
        tap_response = requests.post(
        'https://api.hamsterkombatgame.io/clicker/tap',
        headers={
            'Content-Type': 'application/json',
            'Authorization': authorization
        },
        json={
            'availableTaps': taps-count,
            'count': count,
            'timestamp': int(time.time())
        }
    )
    except Exception as e:
        send_to_TG (e, chat_id = chat_id, bot_token = bot_token)
    try:
        if tap_response.status_code == 200:
            formatted_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
            raw_balance = int(tap_response.json().get('clickerUser', {}).get("balanceCoins", 0))+count
            balance = f"{raw_balance:,}".replace(",", "'")
            send_to_TG (f"[{formatted_date}]\nResponse on {count} taps successfully posted.\nBalance - <b>{balance}</b>", chat_id = chat_id, bot_token = bot_token)
    except Exception:
        print(Exception)
    time.sleep(1)
    buy_best_upgrade()
    time.sleep(589)