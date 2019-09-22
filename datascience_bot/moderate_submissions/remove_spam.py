# -*- coding: utf-8 -*-
"""Remove spam posts from the subreddit
"""
import logging
import os
from typing import Coroutine

import praw


logger = logging.getLogger(__name__)


# define blacklisted domains
VIDEO_URLS = ["youtube.com", "youtu.be", "vid.me"]
BLOG_URLS = ["towardsdatascience.com", "medium.com"]
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
BLACKLISTED_URLS = VIDEO_URLS + BLOG_URLS + PORN_URLS


def remove_spam_submission(submission: praw.models.reddit.submission) -> None:
    """Remove submission that links to spam and reply with explanation
    or constructive advice if warranted.

    Args:
        submission (praw.models.reddit.submission): Submission to remove as
            spam
    """
    logger.debug("Enter remove_spam_submission")

    # Remove videos without comment
    if any(url in submission.url for url in BLACKLISTED_URLS):
        submission.mod.remove(spam=True)
        logger.info(
            f"Removed submission {submission.id} by u/{submission.author} "
            f"from r/{submission.subreddit.display_name}; "
            f"{submission.permalink}"
        )
    else:
        return None

    # Reply with explanation or constructive advice if warranted.

    # Remove porn without comment
    if any(url in submission.url for url in PORN_URLS):
        pass

    # Remove video and explain
    elif any(url in submission.url for url in VIDEO_URLS):
        comment = submission.reply(
            "Your submission has been automatically removed. "
            f"Videos are not allowed in r/{submission.subreddit.display_name}."
        )
        comment.mod.distinguish(how="yes", sticky=True)

    # Remove blog posts and comment alternative
    elif any(url in submission.url for url in BLOG_URLS):
        comment = submission.reply(
            "Your submission has been automatically removed. "
            f"r/{submission.subreddit.display_name} receives a lot of spam "
            "from that domain. Try sharing the original article and offer "
            "context for discussion in the title of your submission."
        )
        comment.mod.distinguish(how="yes", sticky=True)

    else:
        logger.warning(
            "The given submission exists in BLACKLISTED_URLS, but none of the "
            "constituent lists. This is a programming error."
        )

    logger.debug("Exit remove_spam_submission")


if __name__ == "__main__":
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    # if SUBREDDIT_NAME != "datascience_bot_dev":
    #     raise Exception("Test only against r/datascience_bot_dev!")

    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    for submission in subreddit.new(limit=100):
        remove_spam_submission(submission)
