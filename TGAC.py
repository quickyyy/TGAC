import requests
from pathlib import Path
import sys
import os
import time
import configparser
from colorama import Fore, Style
from datetime import datetime
import concurrent.futures
import queue
#Не смотри в код, я тут насрал
#Коменты для себя я делал, кому не нравится идите нахуй
dupedtokens = 0
badtokens = 0
goodtokens = 0
checkedtokens = 0
config = configparser.ConfigParser()
config.read('config.ini')
lang = config.get("Lang", 'lang')
#Ладно смотри: тут мейн функция, тут происходит все и разом
def main():
    os.system('cls')
    print("Welcome to TGAC!\n Developer - https://zelenka.guru/quka/ Github - https://github.com/quickyyy/TGAC")

    config = configparser.ConfigParser()
    config.read('config.ini')

    source_option = input("Select an option:\n1. Parse from folders\n2. Specify a directory with Tokens.txt\nChoice: ")
    num_threads = int(input("Enter the number of threads to run token verification: "))
    if source_option == '1':
        directory = input("Enter the results of blt checker directory (If not specified, the script directory will be checked): ")
        if directory == "":
            directory = os.getcwd()
        path = Path(directory)
        token_files = list(path.glob("**/tokens.txt"))
    elif source_option == '2':
        directory = input('Input a directory with tokens.txt file: ')
        token_files = [Path(directory) / 'tokens.txt']
    else:
        print('Please, enter a correct option.')
        return
    log_info("Starting checker..")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for file_path in token_files:
            with open(file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            if len(lines) % num_threads == 0:
                chunk_size = len(lines) // num_threads
            else:
                chunk_size = len(lines) // num_threads + 1

            chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

            # Split lines among threads evenly
            #chunk_size = len(lines) // num_threads
            #chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

            futures = []
            for chunk in chunks:
                future = executor.submit(process_tokens_chunk, chunk)
                futures.append(future)

            # Wait for all threads to finish
            concurrent.futures.wait(futures)
            #print("The job is done! Report: ")
def mainRu():
    os.system('cls')
    print("Добро пожаловать в TGAC!\n Разработчик - https://zelenka.guru/quka/ Github - https://github.com/quickyyy/TGAC")

    config = configparser.ConfigParser()
    config.read('config.ini')

    source_option = input("Выберите режим работы:\n1. Брать c папок\n2. Выбрать отдельно директорию c tokens.txt\nВыбор: ")
    
    if source_option == '1':
        directory = input("Введите директорию с результатами чекера, где содержаться tokens.txt (Если оставить пустым, будет выбрана директория скрипта): ")
        if directory == "":
            directory = os.getcwd()
        path = Path(directory)
        token_files = list(path.glob("**/tokens.txt"))
    elif source_option == '2':
        directory = input('Введите директорию с tokens.txt: ')
        token_files = [Path(directory) / 'tokens.txt']
    else:
        print('Please, enter a correct option.')
        return
    num_threads = int(input("Введите, в сколько потоков мне работать: "))
    log_info("Начинаю работу..")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for file_path in token_files:
            with open(file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            if len(lines) % num_threads == 0:
                chunk_size = len(lines) // num_threads
            else:
                chunk_size = len(lines) // num_threads + 1

            chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

            # Split lines among threads evenly
            #chunk_size = len(lines) // num_threads
            #chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

            futures = []
            for chunk in chunks:
                future = executor.submit(process_tokens_chunk, chunk)
                futures.append(future)

            # Wait for all threads to finish
            concurrent.futures.wait(futures)
            #print("The job is done! Report: ")
def process_tokens_chunk(chunk):
    goodfunctoken = 0
    badfunctoken = 0
    dupedfunctoken = 0
    config = configparser.ConfigParser()
    config.read('config.ini')
    output_directory = config.get('Paths', 'output_directory')
    output_file = config.get('Paths', 'output_file')
    output_file_bad = config.get('Paths', 'output_file_bad')

    processed_tokens = []
    with open(output_file, 'a', encoding='utf-8') as outfile, open(output_file_bad, 'a', encoding='utf-8') as badfile:
        for line in chunk:
            line = line.replace(u'\ufeff', '').encode('latin-1')
            token = line.strip()
            token = token.decode('utf-8')
            if token in processed_tokens:
                if config.get('Logs', 'show_warnings').lower() == 'true':
                    #log_warning(f"Token is duplicated! {token}")
                    global dupedtokens
                    dupedtokens += 1
                    #global checkedtokens
                    #checkedtokens += 1
                    reroll_info_good(f"Checked", token, processed_tokens)
                    continue

                
                

            result = check_token(token)
            if result == 'good':
                #log_info(f"Good token {Fore.GREEN}{token}{Style.RESET_ALL} Total: {Fore.GREEN}{goodfunctoken}{Style.RESET_ALL} {Fore.RED}{badfunctoken}{Style.RESET_ALL} {Fore.YELLOW}{dupedfunctoken}{Style.RESET_ALL}")
                #log_info(f"Good token: {token} {reroll_info_good(token=token)}")
                reroll_info_good(f"Checked", token, processed_tokens)
                global goodtokens
                goodtokens += 1
                #global checkedtokens
                #checkedtokens += 1
                processed_tokens.append(token)
                outfile.write(f'{token}\n')
                outfile.flush()
            else:
                #log_error(f"Bad token! {Fore.RED}{token}{Style.RESET_ALL}")
                reroll_info_good(f"Checked", token, processed_tokens)
                global badtokens
                badtokens += 1
                #global checkedtokens
                #checkedtokens += 1
                badfile.write(f'{token}\n')
                badfile.flush()



    
    

#Оформление
def the_end(message, token, processed_tokens): #Забудешь ведь все, хуесос! У тебя на 63 строчке валяется почти конец обновы, просто допиши отчет о работе, а потом думай, продавать эту хуйню, либо лучше нинадо
    #P.s. Допиши эту функцию, ей тут одиноко
    #Тут нужен только визуал
    print('Затычка обновления, чтобы не было ерроров при запуске')
    #
    #
def reroll_info_good(message, token, processed_tokens):
    result = check_token(token)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    checkedtokens = goodtokens + badtokens + dupedtokens
    total_info = f"Total: {Fore.GREEN}{goodtokens}{Style.RESET_ALL} {Fore.RED}{badtokens}{Style.RESET_ALL} {Fore.YELLOW}{dupedtokens}{Style.RESET_ALL} {Fore.BLACK}Total checked: {checkedtokens}{Style.RESET_ALL}"
    if result == 'good':
        print(f"{Fore.GREEN}[Good {timestamp}] {token} {Style.RESET_ALL} {message} {total_info}", end=" \r")
    elif result == 'bad':
        print(f"{Fore.RED}[Bad {timestamp}] {token}{Style.RESET_ALL} {message} {total_info}", end=" \r")
    elif token in processed_tokens:
        print(f"{Fore.YELLOW}[Duped {timestamp}] duped token - {token}{Style.RESET_ALL} {message} {total_info}", end=" \r")
def actual_info():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_info = f"Total: {Fore.GREEN}{goodtokens}{Style.RESET_ALL} {Fore.RED}{badtokens}{Style.RESET_ALL} {Fore.YELLOW}{dupedtokens}{Style.RESET_ALL}"
    print(f"{Style.RESET_ALL} {total_info}", end="\r")
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
        if lang != 'ru'.lower():
            main()
        elif lang == 'ru'.lower():
            mainRu()
    except KeyboardInterrupt:
        print("Get ctrl+c!")
        print(f"Thanks for using me! Stat for this check: good - {goodtokens}, bad - {badtokens}, duplicated - {dupedtokens}")
        time.sleep(5)
        pass
