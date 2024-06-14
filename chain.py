from requests.adapters import HTTPAdapter, Retry
import requests
import random
import time

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_new_token(query_id):
    headers_token = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9,en-ID;q=0.8,en;q=0.7,en-US;q=0.6',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://db4.onchaincoin.io',
        'priority': 'u=1, i',
        'referer': 'https://db4.onchaincoin.io/',
        'sec-ch-ua': '""',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36',
    }

    json_data_token = {
        'hash': query_id,
    }
    
    response = session.post('https://db4.onchaincoin.io/api/validate', headers=headers_token, json=json_data_token)
    response_data = response.json()
    return response_data['token']

def refil_energy(auth_token):
    headers_refill = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9,en-ID;q=0.8,en;q=0.7,en-US;q=0.6',
        'authorization': f'Bearer {auth_token}',
        'dnt': '1',
        'origin': 'https://db4.onchaincoin.io',
        'priority': 'u=1, i',
        'referer': 'https://db4.onchaincoin.io/boost',
        'retry-count': '10',
        'sec-ch-ua': '""',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 8 Build/TQ3A.230901.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.123 Mobile Safari/537.36',
    }

    json_data_refill = {}
    while True:
        response_refill = session.post('https://db4.onchaincoin.io/api/boosts/energy', headers=headers_refill, json=json_data_refill)
        if 'Too Many Requests' in response_refill.text:
            print(response_refill.text)
        elif 'No refills left' in response_refill.text:
            status_refill = response_refill.text
            break
        else:
            get_refill_data = response_refill.json()
            status_refill = get_refill_data['status']
            break
    return status_refill



def main():
    query_id = input("Input Your query_id : ")
    auth_token = get_new_token(query_id)

    while True:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-ID;q=0.8,en;q=0.7,en-US;q=0.6',
            'authorization': f'Bearer {auth_token}',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://db4.onchaincoin.io',
            'priority': 'u=1, i',
            'referer': 'https://db4.onchaincoin.io/',
            'sec-ch-ua': '""',
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
            response = session.post('https://db4.onchaincoin.io/api/klick/myself/click', headers=headers, json=json_data)
            response_data = response.json()
            
            if 'error' in response_data:
                error = response_data['error']
                print(error)
                refill_energy = refil_energy(auth_token)
                print(refill_energy)
                if 'No refills left' in refill_energy:
                    delay = random.randint(86400, 87500)
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
