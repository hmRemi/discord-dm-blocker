import os
import time

import requests
from colorama import Fore

class DiscordAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US',
            'authorization': f'{token}',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9147 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Berlin',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTQ3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MzEiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTQ3IENocm9tZS8xMjAuMC42MDk5LjI5MSBFbGVjdHJvbi8yOC4yLjEwIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIyOC4yLjEwIiwiY2xpZW50X2J1aWxkX251bWJlciI6Mjk1MzA2LCJuYXRpdmVfYnVpbGRfbnVtYmVyIjo0ODAxOCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
        }

    def send_message(self, channel_id, message):
        json_data = {'content': message}
        response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=self.headers, json=json_data)
        return response

    def block_user(self, user_id):
        json_data = {'type': 2}
        response = requests.put(f'https://discord.com/api/v9/users/@me/relationships/{user_id}', headers=self.headers, json=json_data)
        return response

    def get_user_info(self, user_id):
        response = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers=self.headers)
        return response.json()


class DiscordMessageSender:
    def __init__(self, token, channel_id, user_id, message, delay=1):
        self.discord_api = DiscordAPI(token)
        self.channel_id = channel_id
        self.user_id = user_id
        self.message = message
        self.delay = delay

    def start_necessary_checks(self):
        """
        Checks if the user has been blocked
        :return: None
        """
        response = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{user_id}", headers=self.discord_api.headers)
        print(f"{prefix} User has been unblocked | {Fore.RED}{response.status_code}")

    def send_message_and_block_user(self):
        response = self.discord_api.send_message(self.channel_id, self.message)
        while True:
            if response.status_code == 200:
                print(f"{prefix} Successfully sent message | {Fore.RED}{response.status_code}")
                self.discord_api.block_user(self.user_id)
                print(f"{prefix} User has been blocked.")
                break
            else:
                response_msg = response.json().get("message", "")
                if response_msg == "Cannot send messages to this user":
                    print(f"{prefix} You are blocked by the user. | {Fore.RED}{response.status_code}")
                else:
                    print(f"{prefix} Failed to send message {response.text} | {Fore.RED}{response.status_code}")
                time.sleep(delay)

    def print_info(self):
        user_info = self.discord_api.get_user_info(self.user_id)
        username = user_info['username']
        print(f'{prefix} Target: {username}')
        print(f'{prefix} User ID: {self.user_id}')
        print(f'{prefix} Channel ID: {self.channel_id}')
        print(f'{prefix} Message: {self.message}')
        print(f'{prefix} Delay: {self.delay}')
        print()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    banner = f"""{Fore.WHITE}
    {Fore.WHITE}██████╗  {Fore.RED}███╗   ███╗    {Fore.WHITE}██████╗  ██╗      ██████╗   ██████╗ ██╗  ██╗ ███████╗ ██████╗
    {Fore.WHITE}██╔══██╗ {Fore.RED}████╗ ████║    {Fore.WHITE}██╔══██╗ ██║     ██╔═══██╗ ██╔════╝ ██║ ██╔╝ ██╔════╝ ██╔══██╗
    {Fore.WHITE}██║  ██║ {Fore.RED}██╔████╔██║    {Fore.WHITE}██████╔╝ ██║     ██║   ██║ ██║      █████╔╝  █████╗   ██████╔╝
    {Fore.WHITE}██║  ██║ {Fore.RED}██║╚██╔╝██║    {Fore.WHITE}██╔══██╗ ██║     ██║   ██║ ██║      ██╔═██╗  ██╔══╝   ██╔══██╗
    {Fore.WHITE}██████╔╝ {Fore.RED}██║ ╚═╝ ██║    {Fore.WHITE}██████╔╝ ███████╗╚██████╔╝ ╚██████╗ ██║  ██╗ ███████╗ ██║  ██║
    {Fore.WHITE}╚═════╝  {Fore.RED}╚═╝     ╚═╝    {Fore.WHITE}╚═════╝  ╚══════╝ ╚═════╝   ╚═════╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝  ╚═╝
                                    Developed by {Fore.RED}Remi{Fore.WHITE} | {Fore.RED}1.0.0{Fore.WHITE}
                                    
    """

    print(banner + Fore.RESET)


class DiscordMessenger:
    def __init__(self, token, channel_id, user_id, message, delay=1):
        self.message_sender = DiscordMessageSender(token, channel_id, user_id, message, delay)

    def start(self):
        clear_console()
        print_banner()
        self.message_sender.print_info()

        print(f"{prefix} Running necessary checks before starting...")
        self.message_sender.start_necessary_checks()

        print()
        print(f"{prefix} Starting the process...")
        self.message_sender.send_message_and_block_user()


prefix = f"{Fore.WHITE}[{Fore.RED}+{Fore.WHITE}]{Fore.RESET}"


if __name__ == '__main__':
    token = ""
    channel_id = ""
    user_id = ""
    message = ""
    prefix = f"{Fore.WHITE}[{Fore.RED}+{Fore.WHITE}]{Fore.RESET}"
    delay = 1

    messenger = DiscordMessenger(token, channel_id, user_id, message, delay)
    messenger.start()

