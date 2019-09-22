# -*- coding: utf-8 -*-
from datetime import datetime
import os

import praw
import pytest


TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def remove_all_datascience_bot_dev_submissions():
    """Remove all submissions in r/datascience_bot_dev before all tests

    https://stackoverflow.com/a/17844938
    """
    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot testing")
    subreddit = reddit.subreddit("datascience_bot_dev")
    for submission in subreddit.new(limit=1000):
        comment = submission.reply(
            f"This submission was removed at {TEST_TIME} to make way for testing."
        )
        comment.mod.distinguish(how="yes", sticky=True)
        submission.mod.remove(spam=False)


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    remove_all_datascience_bot_dev_submissions()
