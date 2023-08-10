import requests
from pathlib import Path
import sys
import os
import time
import configparser
from colorama import Fore, Style
from datetime import datetime

#Не смотри в код, я тут насрал
#Коменты для себя я делал, кому не нравится идите нахуй



#Ладно смотри: тут мейн функция, тут происходит все и разом
def main():
    os.system('cls')
    print("Welcome to TGAC!\n Developer - https://zelenka.guru/quka/ Github - https://github.com/quickyyy/TGAC")

    config = configparser.ConfigParser()
    config.read('config.ini')

    source_option = input("Select an option:\n1. Parse from folders\n2. Specify a directory with Tokens.txt\nChoice: ")

    if source_option == '1':
        directory = input('Enter the results of blt checker directory (If not specified, the script directory will be checked): ')
        if directory == '':
            directory = os.getcwd()
    elif source_option == '2':
        directory = input("Enter the directory containing tokens.txt: ")
    else:
        print("Invalid option. Exiting.")
        return
    
    #Не спрашивай, почему переменные тут.

    goodtokens = 0
    badtokens = 0
    dupedtokens = 0
    processed_tokens = []
    output_directory = config.get('Paths', 'output_directory')
    output_file = config.get('Paths', 'output_file')
    output_file_bad = config.get('Paths', 'output_file_bad')

    #Заносим результаты

    with open(output_file, 'a', encoding='utf-8') as outfile:
        with open(output_file_bad, 'a', encoding='utf-8') as badfile:
            path = Path(directory)
            token_files = list(path.glob('**/tokens.txt'))

            for file_path in token_files:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        line = line.replace(u'\ufeff', '').encode('latin-1')
                        token = line.strip()
                        token = token.decode('utf-8')
                        if token in processed_tokens:
                            if config.get('Logs', 'show_warnings').lower() == 'true':
                                log_warning(f"Token is duplicated! {token}")
                                dupedtokens += 1
                            continue 

                        result = check_token(token)
                        if result == 'good':
                            log_info(f"Good token {Fore.GREEN}{token}{Style.RESET_ALL}")
                            goodtokens += 1
                            processed_tokens.append(token)
                            outfile.write(f'{token}\n')  
                            outfile.flush() 
                        else:
                            log_error(f"Bad token! {Fore.RED}{token}{Style.RESET_ALL}")
                            badtokens += 1
                            badfile.write(f'{token}\n') 
                            badfile.flush()  
    
    

#Оформление
def log_info(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}[INFO {timestamp}]{Style.RESET_ALL} {message}")
def log_warning(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.YELLOW}[WARNING {timestamp}]{Style.RESET_ALL} {message}")
def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.RED}[ERROR {timestamp}]{Style.RESET_ALL} {message}")



#чекаем токены
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


#Запускаем скрипт
if __name__ == "__main__":
    outfile = None
    badfile = None
    
    try:
        main()
    except KeyboardInterrupt:
        pass
