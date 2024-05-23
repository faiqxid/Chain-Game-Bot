import requests
import random
import time

def get_new_token(query_id):
    headers_token = {
        'authority': 'db4.onchaincoin.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'referer': 'https://db4.onchaincoin.io/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36',
    }

    json_data_token = {
        'hash': query_id,
    }
    
    response = requests.post('https://db4.onchaincoin.io/api/validate', headers=headers_token, json=json_data_token)
    response_data = response.json()
    return response_data['token']

def main():
    query_id = input("Input Your query_id : ")
    auth_token = get_new_token(query_id)

    while True:
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
        
        random_num = random.randint(1, 50)
        json_data = {
            'clicks': random_num,
        }
        
        try:
            response = requests.post('https://db4.onchaincoin.io/api/klick/myself/click', headers=headers, json=json_data)
            response_data = response.json()
            
            if 'error' in response_data:
                error = response_data['error']
                print(error)
                rand_delay = random.randint(60, 120)
                delay = rand_delay * 60
                for i in range(delay, 0, -1):
                    minutes, seconds = divmod(i, 60)
                    hours, minutes = divmod(minutes, 60)
                    print(f"Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}", end='\r')
                    time.sleep(1)
            else:
                energy = response_data['energy']
                coins = response_data['coins']
                print('Remaining Energy ' + str(energy) + ' Your Coins ' + str(coins))
                time.sleep(5)
        
        except Exception as e:
            print('An error occurred:', e)
            try:
                message = response_data.get('message', '')
                if 'Invalid token' in message:
                    print(message + " Your Token Maybe Expired")
                    auth_token = get_new_token(query_id)
            except Exception as e:
                print('Retrying due to error:', e)
                time.sleep(2)

if __name__ == "__main__":
    main()
