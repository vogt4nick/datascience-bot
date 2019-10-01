# -*- coding: utf-8 -*-
from datetime import datetime
import os

import praw
import pytest


TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


@pytest.fixture
def datascience_bot_reddit() -> praw.reddit:
    """Create a reddit instance with u/datascience-bot

    Returns:
        praw.models.reddit: A reddit instance with u/datascience-bot
    """
    return praw.Reddit(
        username=os.getenv("DATASCIENCE_BOT_USERNAME"),
        password=os.getenv("DATASCIENCE_BOT_PASSWORD"),
        client_id=os.getenv("DATASCIENCE_BOT_CLIENT_ID"),
        client_secret=os.getenv("DATASCIENCE_BOT_CLIENT_SECRET"),
        user_agent="datascience-bot",
    )


@pytest.fixture
def SubstantialStrain6_reddit() -> praw.models.reddit:
    """Create a reddit instance with u/SubstantialStrain6

    Returns:
        praw.models.reddit: A reddit instance with u/SubstantialStrain6
    """
    return praw.Reddit(
        username=os.getenv("SUBSTANTIALSTRAIN6_USERNAME"),
        password=os.getenv("SUBSTANTIALSTRAIN6_PASSWORD"),
        client_id=os.getenv("SUBSTANTIALSTRAIN6_CLIENT_ID"),
        client_secret=os.getenv("SUBSTANTIALSTRAIN6_CLIENT_SECRET"),
        user_agent="SubstantialStrain6",
    )


@pytest.fixture
def b3405920_reddit() -> praw.models.reddit:
    """Create a reddit instance with u/b3405920

    Returns:
        praw.models.reddit: A reddit instance with u/b3405920
    """
    return praw.Reddit(
        username=os.getenv("B3405920_USERNAME"),
        password=os.getenv("B3405920_PASSWORD"),
        client_id=os.getenv("B3405920_CLIENT_ID"),
        client_secret=os.getenv("B3405920_CLIENT_SECRET"),
        user_agent="b3405920",
    )


def remove_all_user_submissions_to_datascience_bot_dev():
    datascience_bot = praw.Reddit(
        username=os.getenv("DATASCIENCE_BOT_USERNAME"),
        password=os.getenv("DATASCIENCE_BOT_PASSWORD"),
        client_id=os.getenv("DATASCIENCE_BOT_CLIENT_ID"),
        client_secret=os.getenv("DATASCIENCE_BOT_CLIENT_SECRET"),
        user_agent="datascience-bot",
    )
    SubstantialStrain6 = praw.Reddit(
        username=os.getenv("SUBSTANTIALSTRAIN6_USERNAME"),
        password=os.getenv("SUBSTANTIALSTRAIN6_PASSWORD"),
        client_id=os.getenv("SUBSTANTIALSTRAIN6_CLIENT_ID"),
        client_secret=os.getenv("SUBSTANTIALSTRAIN6_CLIENT_SECRET"),
        user_agent="SubstantialStrain6",
    )
    b3405920 = praw.Reddit(
        username=os.getenv("B3405920_USERNAME"),
        password=os.getenv("B3405920_PASSWORD"),
        client_id=os.getenv("B3405920_CLIENT_ID"),
        client_secret=os.getenv("B3405920_CLIENT_SECRET"),
        user_agent="b3405920",
    )

    for reddit in (datascience_bot, SubstantialStrain6, b3405920):
        username = reddit.user.me().name
        # remove all submissions to /r/datascience_bot_dev
        for submission in reddit.redditor(username).submissions.new(limit=100):
            if submission.subreddit.display_name == "datascience_bot_dev":
                submission.delete()

        # remove all comments on /r/datascience_bot_dev
        for comment in reddit.redditor(username).comments.new(limit=100):
            if comment.subreddit.display_name == "datascience_bot_dev":
                comment.delete()


def remove_all_datascience_bot_dev_submissions():
    """Remove all submissions in r/datascience_bot_dev before all tests

    https://stackoverflow.com/a/17844938
    """
    reddit = praw.Reddit(
        username=os.getenv("DATASCIENCE_BOT_USERNAME"),
        password=os.getenv("DATASCIENCE_BOT_PASSWORD"),
        client_id=os.getenv("DATASCIENCE_BOT_CLIENT_ID"),
        client_secret=os.getenv("DATASCIENCE_BOT_CLIENT_SECRET"),
        user_agent="datascience-bot",
    )
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


if __name__ == "__main__":
    remove_all_user_submissions_to_datascience_bot_dev()
