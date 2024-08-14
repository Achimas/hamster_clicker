import os
import time
import random
import requests
from dotenv import load_dotenv

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

    response = requests.post('https://api.hamsterkombatgame.io/clicker/upgrades-for-buy', headers=headers).json()
    upgrades = [
        item for item in response["upgradesForBuy"]
        if not item["isExpired"] and item["isAvailable"] and item["price"] > 0
    ]

    most_efficient_upgrade = ["", 0, 0]
    for i in upgrades:
        try: a = i["toggle"]
        except:
            id = i["id"]
            efficiency_coeff = i["profitPerHour"]/i["price"]
            price = i["price"]
        if efficiency_coeff > most_efficient_upgrade[1]:
            most_efficient_upgrade[0] = id
            most_efficient_upgrade[1] = efficiency_coeff
            most_efficient_upgrade[2] = f"{price:,}".replace(",", "'")
    upgrade_id = most_efficient_upgrade[0]
    timestamp = int(time.time() * 1000)
    url = "https://api.hamsterkombatgame.io/clicker/buy-upgrade"
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
        "Origin": "https://hamsterkombat.io",
        "Referer": "https://hamsterkombat.io/"
    }
    data = {
        "upgradeId": upgrade_id,
        "timestamp": timestamp
    }
    response = requests.post(url, headers=headers, json=data)
    formatted_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
    if response.status_code == 200:
        print (f"[{formatted_date}] Upgrade {most_efficient_upgrade[0]} is purcashed. Price {most_efficient_upgrade[2]}")
        return True
    if response.status_code == 400:
        print (f"[{formatted_date}] Upgrade {most_efficient_upgrade[0]} cannot be percashed. Price {most_efficient_upgrade[2]}")

# Ввод токена авторизации
# Ввод порога вместимости монет
load_dotenv()
authorization = os.getenv("authorization")
# В моем случае предел равен 7000
try: load_capacity =  os.getenv("capacity")
except: load_capacity = None
capacity = int(load_capacity)-2000 if load_capacity else 900

while True:
    # Получаем количество доступных тапов
    response = requests.post(
        'https://api.hamsterkombatgame.io/clicker/sync',
        headers={
            'Content-Type': 'application/json',
            'Authorization': authorization
        },
        json={}
    )
    try: taps = response.json().get('clickerUser', {}).get('availableTaps', 0)
    except Exception as e: print(e)

    # Если тапов меньше 30, ждем пока их количество не достигнет capacity
    if taps < 30:
        formatted_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
        print(f"[{formatted_date}] Taps are less than 30. Waiting to reach {capacity} again...")
        while taps < capacity:
            formatted_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
            response = requests.post(
                'https://api.hamsterkombatgame.io/clicker/sync',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': authorization
                },
                json={}
            )
            if response.status_code == 200:
                try: taps = response.json().get('clickerUser', {}).get('availableTaps', 0)
                except Exception as e: print(f"[{formatted_date}] Error - {e}")
                else: print(f"[{formatted_date}] Available taps - {taps}")
            time.sleep(420)
        continue

    # Пауза на случайное время между 20 и 60 миллисекундами
    random_sleep = random.uniform(20, 60) / 1000
    time.sleep(random_sleep)

    count = int(random.uniform(0, taps))

    # Отправляем запрос для выполнения тапов
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
    if tap_response.status_code == 200:
        formatted_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
        raw_balance = int(tap_response.json().get('clickerUser', {}).get("balanceCoins", 0))+count
        balance = f"{raw_balance:,}".replace(",", "'")
        print (f"[{formatted_date}] Response on {count} taps successfully posted. Balance - {balance}")

    money_enough = True
    while money_enough:
        money_enough = buy_best_upgrade()