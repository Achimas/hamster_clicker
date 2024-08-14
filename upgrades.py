import os
import requests
from dotenv import load_dotenv
import time 

load_dotenv()
authorization = os.getenv("authorization")

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


if __name__ == "__main__":
    buy_best_upgrade()

# {'id': 'healthy_hamster', 'name': 'Healthy nutrition hamster', 'releaseAt': '2024-08-06T11:00:00.000Z', 'price': 12331170, 'profitPerHour': 22313, 'condition': None, 'cooldownSeconds': 0, 'section': 'Specials', 'level': 16, 'currentProfitPerHour': 20106, 'profitPerHourDelta': 2207, 'isAvailable': True, 'isExpired': False, 'totalCooldownSeconds': 7200}