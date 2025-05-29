#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
## Created by https://github.com/bergamot88
##

import argparse
import os
import json
import sys
import yaml
import asyncio
from service.vk_service import VKService
from service.telegram_service import TelegramService
from argparse import Namespace
from rich.console import Console
from rich.theme import Theme
from tqdm import tqdm
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
from pathlib import Path


custom_theme = Theme({
    'info': 'cyan',
    'warning': 'magenta',
    'success': 'bold green',
    'error': 'bold red'
})
console = Console(theme=custom_theme)


def get_parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Check VK video comments for specific words')
    parser.add_argument('-u', '--url', type=str, help='VK video or Telegram post URL')
    parser.add_argument('-k', '--keywords', type=str, nargs='+', help='Keywords to search for')
    parser.add_argument('-c', '--config', type=str, help='Path to config file (JSON or YAML)')
    parser.add_argument('-s', '--save-output-to-file', type=str, help='Output file path (.json or .txt)')
    parser.add_argument('-vk', '--vk-token', type=str, help='VK token')
    parser.add_argument('-tg-i', '--tg-api-id', type=str, help='Telegram API ID')
    parser.add_argument('-tg-h', '--tg-api-hash', type=str, help='Telegram API Hash')
    return parser.parse_args()


def load_config(config_path: str) -> Dict:
    with open(config_path, 'r', encoding='utf-8') as f:
        if config_path.endswith('.json'):
            return json.load(f)
        elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
            return yaml.safe_load(f)
        else:
            raise ValueError('Unsupported config file format. Use JSON or YAML.')


def load_env_vars():
    dotenv_file = Path(__file__).parent / 'configs' / '.env'
    if dotenv_file.exists():
        load_dotenv(dotenv_file)


def determine_platform(vk_token: Optional[str], tg_api_id: Optional[Any], tg_api_hash: Optional[Any]) -> Optional[str]:
    if vk_token:
        return 'vk'
    elif tg_api_id and tg_api_hash:
        return 'telegram'
    return None


def save_comments_to_file(comments: List, output_file_path: str):
    console.print(f"\n[info]▶✒️ Write response output to file {output_file_path} [/]")
    output_file_path: Path = Path(output_file_path)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        if output_file_path.suffix == '.json':
            with open(output_file_path.with_suffix('.json'), 'w', encoding='utf-8') as file:
                json.dump(comments, file, indent=4, ensure_ascii=False)
        elif output_file_path.suffix == '.txt':
            for item in comments:
                file.write(f"{item}\n")


def main() -> None:
    args: Namespace = get_parse_args()
    load_env_vars()

    config: Dict = {}
    if args.config:
        config = load_config(args.config)

    url: Optional[str] = args.url or config.get("url")
    keywords: Optional[List[str]] = args.keywords or config.get("keywords")
    vk_token: Optional[str] = args.vk_token or config.get("vk_token") or os.getenv('VK_TOKEN')
    tg_api_id: Optional[int] = args.tg_api_id or config.get("tg_api_id") or os.getenv('TELEGRAM_API_ID')
    tg_api_hash: Optional[str] = args.tg_api_hash or config.get("tg_api_hash") or os.getenv('TELEGRAM_API_HASH')
    output_file_path: Optional[str] = args.save_output_to_file or config.get("save_output_to_file")
    platform: str = ''

    if not url or not keywords:
        console.print('\n[error]❌ Missing required parameters[/]')
        console.print('\t[warning]⚠️ You need to provide:[/]')
        console.print('\t\t[info]1. URL (use --url)[/]')
        console.print('\t\t[info]2. Words to search (use --keywords)[/]')
        sys.exit(1)

    if not vk_token and not tg_api_id and not tg_api_hash:
        console.print('\n[error]❌ Missing required parameters[/]')
        console.print('\t[warning]⚠️ You need to provide:[/]')
        console.print('\t\t[info]1. Access token (use --vk-token or --tg-api-id and --tg-api-hash)[/]')
        sys.exit(1)
        
    platform = determine_platform(vk_token, tg_api_id, tg_api_hash)

    if platform is None:
        console.print('\n[error]❌ Platform is not defined [/]')
        sys.exit(1)
    elif platform == 'vk':
        vk_service = None
        try:
            vk_service = VKService(vk_token, console)
        except Exception as e:
            console.print(f"\n[error]❌Error: {e}[/]")
            sys.exit(1)

        console.print(f"\n[info]▶🔄 Fetching comments for video {url}[/]")
        comments: List = vk_service.fetch_all_video_comments(url)
        if len(comments):
            console.print(f"\t[info]▶✅ Found {len(comments)} comments (including threads)[/]")
        else:
            console.print(f"\t[info]❌ No found {len(comments)} comments (including threads)[/]")

        console.print('\n[info]▶🔍 Searching for keywords...[/]')
        matched_count: List = vk_service.filter_comments_by_keywords(comments, keywords)
        
        if len(matched_count):
            console.print(f"\t[info]▶✅ Found {len(matched_count)} matches for {' '.join(keywords)} [/]")
            for count in matched_count:
                console.print(f"\t\t[info]▶📍 {count} [/]")
        else:
            console.print(f"\t[info]▶❌ Not found matches for {' '.join(keywords)} [/]")

        if output_file_path is not None:
            save_comments_to_file(comments, output_file_path)
    elif platform == 'telegram':
        console.print("[info]Telegram support is not implemented yet.[/]")


if __name__ == '__main__':
    main()
