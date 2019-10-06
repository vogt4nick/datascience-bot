# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os

import praw
import pytest

from datascience_bot import get_datascience_bot, get_SubstantialStrain6, get_b3405920


TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


def remove_all_user_submissions_to_datascience_bot_dev():
    datascience_bot = get_datascience_bot()
    SubstantialStrain6 = get_SubstantialStrain6()
    b3405920 = get_b3405920()

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
    reddit = get_datascience_bot()

    subreddit = reddit.subreddit("datascience_bot_dev")
    for submission in subreddit.new(limit=1000):
        comment = submission.reply(
            f"This submission was removed at {TEST_TIME} to make way for testing."
        )
        comment.mod.distinguish(how="yes", sticky=True)
        submission.mod.remove(spam=False)


def make_existing_thread() -> praw.models.Submission:
    datascience_bot = get_datascience_bot()
    SubstantialStrain6 = get_SubstantialStrain6()
    b3405920 = get_b3405920()

    weekly_thread = datascience_bot.subreddit(SUBREDDIT_NAME).submit(
        title=(
            "Weekly Entering & Transitioning Thread | "
            f"{(datetime.utcnow() - timedelta(days=7)).strftime('%d %b %Y')} - "
            f"{datetime.utcnow().strftime('%d %b %Y')}"
        ).strip(),
        selftext="Testing",
        send_replies=False,
    )
    weekly_thread.mod.approve()
    weekly_thread.mod.distinguish()
    weekly_thread.mod.sticky(state=True, bottom=True)

    # make a comment that will go unanswered
    SubstantialStrain6.submission(id=weekly_thread.id).reply(
        "I have a question that will go unanswered"
    )

    # make a comment and answer it
    comment = b3405920.submission(id=weekly_thread.id).reply(
        "I have a question that will be answered by SubstantialStrain6"
    )
    SubstantialStrain6.comment(id=comment.id).reply("I'm answering your question")

    return weekly_thread


def pytest_sessionstart(session):
    """Called after the Session object has been created and before performing
    collection and entering the run test loop.
    """
    remove_all_datascience_bot_dev_submissions()
    remove_all_user_submissions_to_datascience_bot_dev()
    make_existing_thread()
