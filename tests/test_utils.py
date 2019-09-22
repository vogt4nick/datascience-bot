# -*- coding: utf-8 -*-
from datetime import datetime
import os

import praw
import pytest

from datascience_bot import update, submission_is_deleted, submission_is_removed

TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def test__update():
    reddit = praw.Reddit("SubstantialStrain6", user_agent="datascience-bot testing")
    subreddit = reddit.subreddit(display_name="datascience_bot_dev")

    return None


def test__submission_is_deleted():
    ## Create a post with u/SubstantialStrain6
    user_submission = (
        praw.Reddit("SubstantialStrain6", user_agent="datascience-bot testing")
        .subreddit(display_name="datascience_bot_dev")
        .submit(
            title=f"Test datascience_bot:submission_is_removed | {TEST_TIME}",
            selftext="This is a test.",
            send_replies=False,
        )
    )

    # View u/SubstantialStrain6's post with u/datascience-bot
    mod = praw.Reddit("datascience-bot", user_agent="datascience-bot testing")
    submission = update(user_submission, mod)

    assert submission_is_deleted(submission, mod) == False

    user_submission.delete()

    assert submission_is_deleted(submission, mod) == True


def test__submission_is_removed():
    ## Create a post with u/SubstantialStrain6
    user_submission = (
        praw.Reddit("SubstantialStrain6", user_agent="datascience-bot testing")
        .subreddit(display_name="datascience_bot_dev")
        .submit(
            title=f"Test datascience_bot:submission_is_removed | {TEST_TIME}",
            selftext="This is a test.",
            send_replies=False,
        )
    )

    # View u/SubstantialStrain6's post with u/datascience-bot
    mod = praw.Reddit("datascience-bot", user_agent="datascience-bot testing")
    submission = update(user_submission, mod)

    assert submission_is_removed(submission, mod) == False

    submission.mod.remove(spam=False)

    assert submission_is_removed(submission, mod) == True
