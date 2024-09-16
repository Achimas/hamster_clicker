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

def _take_toppest_upgrades():
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

    best_upgrade_list = [["", int(0), "0"]]
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
                best_upgrade_list.append(top_up)
        except Exception as e:
            print(f"Sth happens wrong in adding to list:\n'{i}'")
            print(e)
    best_upgrade_list.pop(0)
    sorted_upgrades = sorted(best_upgrade_list, key=lambda x: x[1])
    print (sorted_upgrades)
    return sorted_upgrades

def buy_best_upgrade():
    toppest_upgrades = _take_toppest_upgrades()
    
    for up in toppest_upgrades:
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
            price = f"{up[2]:,}".replace(",", "'")
            text = f"Upgrade {up[0]} is purcashed.\nPrice - <b>{price}</b>"
            send_to_TG(text, chat_id=chat_id,
                        bot_token=bot_token)

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

def make_taps(taps, count):
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
        if isinstance(tap_response, requests.Response) and tap_response.status_code == 200:
            raw_balance = int(tap_response.json().get('clickerUser', {}).get("balanceCoins", 0))+count
            balance = f"{raw_balance:,}".replace(",", "'")
            text = f"Response on {count} taps successfully posted.\nBalance - <b>{balance}</b>"
            return text
        else: text = "Taps not posted"
    except Exception as e:
        text = repr(e)
    return text

# загрузка из переменных окружения
load_dotenv()
chat_id = os.getenv("chat_id")
bot_token = os.getenv("bot_token")
authorization = os.getenv("authorization")

while True:
    # Получаем количество доступных тапов
    taps = get_avaliable_taps()
    count = int(random.uniform(0, taps))

    time.sleep(1)

    taps_result = make_taps(taps, count)
    send_to_TG(taps_result, chat_id = chat_id, bot_token = bot_token)

    time.sleep(1)
    buy_best_upgrade()
    time.sleep(589)