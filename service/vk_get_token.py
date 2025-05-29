#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
## Created by https://github.com/bergamot88
##

import os
import requests
import argparse
from argparse import Namespace
from pathlib import Path
from dotenv import load_dotenv


def get_access_token(phone_number: str, password: str, client_id: str, client_secret: str) -> str:
    token_url = 'https://oauth.vk.com/token' 
    params = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': phone_number,
        'password': password
    }
    try:
        response = requests.post(token_url, data=params)
        response.raise_for_status()
        token_data = response.json()
        
        if 'access_token' not in token_data:
            error_desc = token_data.get('error_description', 'Unknow error')
            raise Exception(f"Error receiving token: {error_desc}")
        
        return token_data['access_token']

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network or query error: {e}")


def set_env_variable(key: str, value: str, env_file: Path = '.env') -> None:
    load_dotenv(dotenv_path=env_file)

    env_file.touch(exist_ok=True)

    with open(env_file, 'r') as file:
        lines = file.readlines()

    found = False
    updated_lines = []

    for line in lines:
        if line.startswith(f"{key}="):
            updated_lines.append(f"{key}={value}\n")
            found = True
        else:
            updated_lines.append(line)

    if not found:
        updated_lines.append(f"{key}={value}\n")

    with open(env_file, 'w') as file:
        file.writelines(updated_lines)

    os.environ[key] = value


def get_parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Get VK access token')
    parser.add_argument('--phone', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--client_id', type=str, required=True)
    parser.add_argument('--client_secret', type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args: Namespace = get_parse_args()
    dotenv_file: Path = Path(__file__).parent.parent / 'configs' / '.env'
    token: str = get_access_token(args.phone, args.password, args.client_id, args.client_secret)
    set_env_variable('VK_TOKEN', token, dotenv_file)

if __name__ == '__main__':
    main()
