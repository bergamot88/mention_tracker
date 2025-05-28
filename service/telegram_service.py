#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
## Created by https://github.com/bergamot88
##

import asyncio
import re
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty
from typing import List, Dict, Optional, Union
from rich.console import Console
import time


class TelegramService():
    def __init__(self, tg_api_id: int, tg_api_hash: str, console: Console):
        self.console: Console = console
        self.tg_api_id: int = tg_api_id
        self.tg_api_hash: str = tg_api_hash
