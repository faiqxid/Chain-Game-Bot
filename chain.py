import requests
import random
import time

auth_token = input("Input Your Token Ex.eyjxxxx: ")

headers = {
    'authority': 'db4.onchaincoin.io',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': f'Bearer {auth_token}',
    'content-type': 'application/json',
    'origin': 'https://db4.onchaincoin.io',
    'referer': 'https://db4.onchaincoin.io/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36',
}

while True:
    random_num = random.randint(1, 50)
    json_data = {
        'clicks': random_num,
    }
    try:
        response = requests.post('https://db4.onchaincoin.io/api/klick/myself/click', headers=headers, json=json_data).json()
        try:
            energy = response['energy']
            coins = response['coins']
            print('Remaining Energy ' + str(energy) + ' Your Coins ' + str(coins))
            time.sleep(5)
        except:
            error = response['error']
            print(error)
            rand_delay = random.randint(60, 120)
            delay = rand_delay*30
            for i in range(delay, 0, -1):
                minutes, seconds = divmod(i, 60)
                hours, minutes = divmod(minutes, 60)
                print(f"Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}", end='\r')
                time.sleep(1)
            
    except:
        try:
            message = response['message']
            print(message+" Your Token Mybe Expired")
            if 'Invalid token' in message:
                break
        except:
            print('Try again....')
            time.sleep(2)
