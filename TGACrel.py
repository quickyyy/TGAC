
import requests
from pathlib import Path
import sys
import os
import time
import colorama
from colorama import Fore, Style
from datetime import datetime
def main():
    os.system('cls')
    print("Welcome to TGAC!\n Developer - https://zelenka.guru/quka/ Github - https://github.com/quickyyy/TGAC")
    directory = input('Enter the results directory: ')
    output_file = 'all_tokens.txt'
    output_file_bad = 'bad_tokens.txt'
    goodtokens = 0
    badtokens = 0
    with open(output_file, 'a', encoding='utf-8') as outfile:
        path = Path(directory)
        token_files = list(path.glob('**/tokens.txt'))
        for file_path in token_files:
            with open(file_path, 'r', encoding='utf-8') as infile:
                for line in infile:
                    line = line.replace(u'\ufeff', '').encode('latin-1')
                    token = line.strip() 
                    token = token.decode('utf-8')

                    result = check_token(token)
                    if result == 'good':
                        outfile.write(f'{token}\n')
                        log_info(f"Good token {Fore.GREEN}{token}{Style.RESET_ALL}")
                        #print('good ', token)
                        goodtokens += 1
                    else:
                        log_error(f"Bad token! {Fore.RED}{token}{Style.RESET_ALL}")
                        #print('bad ', token)
                        badtokens += 1
            
            with open(output_file_bad, 'a', encoding='utf-8') as badfile:
                if token == 'bad':
                    badfile.write(f'{token}')
def log_info(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}[INFO {timestamp}]{Style.RESET_ALL} {message}")
def log_warning(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.YELLOW}[WARNING {timestamp}]{Style.RESET_ALL} {message}")
def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.RED}[ERROR {timestamp}]{Style.RESET_ALL} {message}")
def check_token(token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.twitch.tv/',
        'Authorization': f'OAuth {token}',
        'Pragma': 'no-cache',
        'Origin': 'https://twitch.tv',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
    }
    link = 'https://id.twitch.tv/oauth2/validate'
    try:
        response = requests.get(link, headers=headers)
        result = process_response(response)
    except requests.exceptions.RequestException as e:
        result = 'request error'
    return result

def process_response(response):

    if 'client_id' in response.text:
        result = 'good'
    elif 'invalid access token' in response.text:
        result = 'bad'
    return result


if __name__ == "__main__":
    main()
