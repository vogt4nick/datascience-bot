# -*- coding: utf-8 -*-
"""Post the weekly entering & transitioning thread to r/datascience using
u/datascience-bot.
"""
from datetime import datetime, timedelta
import logging
import os
import sys
from typing import Coroutine

import praw

from exceptions import MissingSubmissionError


# config logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# either datascience_bot_dev for testing, or datascience for production
SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")


VIDEO_URLS = ["youtube.com", "youtu.be", "vid.me"]
PORN_URLS = [
    "porn.com",
    "pornhub.com",
    "porntube.com",
    "redtube.com",
    "socialmunch.com",
    "spankwire.com",
    "xhamster.com",
    "xvideos.com",
    "youjizz.com",
    "youporn.com",
    "extremetube.com",
    "hardsextube.com",
]
BLOG_URLS = ["towardsdatascience.com", "medium.com"]

SPAM_URLS = VIDEO_URLS + PORN_URLS + BLOG_URLS


def remove_spam_submissions(subreddit: praw.models.reddit.subreddit) -> None:
    """Remove submissions that link to spam

    Args:
        subreddit (praw.models.reddit.subreddit): Subreddit to look for video
            submissions
    """
    logger.info("Collect spam submissions")

    count_spam_submissions = 0
    for submission in subreddit.new(limit=100):
        if submission.is_self or submission.approved:
            continue
        if any(url in submission.url for url in SPAM_URLS):
            count_spam_submissions += 1
            remove_spam_submission(submission, subreddit)

    logger.info(
        f"Successfully collected all ({count_spam_submissions}) spam submissions"
    )


def remove_spam_submission(
    submission: praw.models.reddit.submission, subreddit: praw.models.reddit.subreddit
) -> None:
    """Remove submission that links to spam

    Args:
        submission (praw.models.reddit.submission): Submission to remove as
            spam
        subreddit (praw.models.reddit.subreddit): Subreddit to look for spam
            submissions
    """
    logger.info(
        f"Remove submission ({submission.id}): "
        f"{submission.title} by u/{submission.author}"
    )

    submission.mod.remove(spam=True)

    if any(url in submission.url for url in VIDEO_URLS):
        submission.reply(
            "Your submission has been automatically removed. "
            f"Videos are not allowed in r/{subreddit.display_name}."
        )
    elif any(url in submission.url for url in PORN_URLS):
        pass
    elif any(url in submission.url for url in BLOG_URLS):
        submission.reply(
            "Your submission has been automatically removed. "
            f"r/{subreddit.display_name} receives a lot of spam from that "
            "domain. Try sharing the original article and offer context for "
            "discussion in the title of your submission."
        )
    else:
        logger.warning("The given submission was not flagged as spam.")

    logger.debug("Successfully removed submission")


def main():
    logger.info("Enter remove_spam.main.py")

    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    logger.info(f"Acting on subreddit: {subreddit.display_name}")

    remove_spam_submissions(subreddit)

    logger.info("Exit remove_spam.main.py")


if __name__ == "__main__":
    main()
