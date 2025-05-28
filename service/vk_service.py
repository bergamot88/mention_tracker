#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
## Created by https://github.com/bergamot88
##

import re
import math
import random
import time
import sys
from typing import List, Dict, Any, Tuple, Optional
import vk_api
from rich.console import Console
from vk_api.exceptions import VkApiError, ApiError


DEFAULT_COMMENTS_PER_REQUEST = 100
DELAY_RANGE = (12, 35)


class VKService:
    def __init__(self, access_token: str, console: Console) -> None:
        self.access_token = access_token
        self.console = console
        self.vk_session = vk_api.VkApi(token=self.access_token)
        self.vk = self.vk_session.get_api()

    def parse_video_url(self, video_url: str) -> Tuple[int, int]:
        """
        Parses a video link and returns owner_id and video_id.
        :raises ValueError: if the link format is incorrect.
        """
        match = re.search(r'video(-?\d+)_(\d+)', video_url)
        if not match:
            raise ValueError("Incorrect video link")
        return int(match.group(1)), int(match.group(2))

    def get_video_comments_count(self, video_url: str) -> int:
        """
        Returns the number of comments on the video.
        """
        owner_id, video_id = self.parse_video_url(video_url)

        try:
            response = self.vk.video.getComments(
                owner_id=owner_id,
                video_id=video_id,
                count=0
            )
            return int(response['count'])
        except ApiError as e:
            self.console.print(f"\n[error]❌ Error VK API: {e}[/]")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"\n[error]❌ Common error: {e}[/]")
            sys.exit(1)
        return 0

    def random_sleep(self) -> float:
        """
        Delay between requests to avoid anti-spam triggering.
        :return: delay time in seconds.
        """
        delay = random.uniform(*DELAY_RANGE)
        time.sleep(delay)
        return delay

    def fetch_all_video_comments(self, video_url: str) -> List[Dict[str, Any]]:
        """
        Gets all the comments on the video with pagination.
        """
        owner_id, video_id = self.parse_video_url(video_url)
        total_comments = self.get_video_comments_count(video_url)

        if total_comments == 0:
            return []

        comments = []
        total_pages = math.ceil(total_comments / DEFAULT_COMMENTS_PER_REQUEST)

        for page in range(total_pages):
            self.random_sleep()
            offset = page * DEFAULT_COMMENTS_PER_REQUEST

            try:
                response = self.vk.video.getComments(
                    owner_id=owner_id,
                    video_id=video_id,
                    count=DEFAULT_COMMENTS_PER_REQUEST,
                    offset=offset,
                    sort="desc",
                    thread_items_count=10
                )

                comments.extend(response.get('items', []))
            except (VkApiError, ApiError) as e:
                self.console.print(f"\n[error]❌ Error when fetching comments: {e}[/]")
                continue

        return comments

    def filter_comments_by_keywords(self, comments: List[Dict], keywords: List[str]) -> List[Dict]:
        """
        Filters comments based on the presence of at least one keyword in any field.
        """
        def contains_keyword(comment: Dict) -> bool:
            comment_text = " ".join(str(value).lower() for value in comment.values())
            return any(keyword.lower() in comment_text for keyword in keywords)

        return [comment for comment in comments if contains_keyword(comment)]
