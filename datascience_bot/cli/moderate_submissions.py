# -*- coding: utf-8 -*-
"""Moderate new submissions as they are posted
"""
from datetime import datetime, timedelta
import logging
import os
import sys
from typing import Coroutine

import praw

from datascience_bot.remove_spam import remove_spam_submission
from datascience_bot.remove_trolls import remove_troll_submission


# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def main() -> None:
    """Remove submissions that link to spam
    """
    logger.info("Collect spam submissions")

    # either datascience_bot_dev for testing, or datascience for production
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")

    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    count_spam_submissions = 0
    for submission in subreddit.new(limit=5):
        count_spam_submissions += 1
        # remove_*_submission functions return true if submission is removed
        if remove_spam_submission(submission):
            continue
        if remove_troll_submission(submission):
            continue

    logger.info(
        f"Successfully collected all ({count_spam_submissions}) spam submissions"
    )


if __name__ == "__main__":
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    if SUBREDDIT_NAME != "datascience_bot_dev":
        raise Exception("Test only against r/datascience_bot_dev!")

    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    main()
