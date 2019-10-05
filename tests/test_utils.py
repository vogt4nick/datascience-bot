# -*- coding: utf-8 -*-
from datetime import datetime
import os

import praw
import pytest

from datascience_bot import (
    add_boilerplate,
    update,
    submission_is_deleted,
    submission_is_removed,
    get_datascience_bot,
    get_SubstantialStrain6,
    get_b3405920,
)

TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def test__add_boilerplate():
    test = "This is a test."
    assert test != add_boilerplate(test)


# def test__update(SubstantialStrain6_reddit):
#     reddit = SubstantialStrain6_reddit
#     subreddit = reddit.subreddit(display_name="datascience_bot_dev")

#     return None


def test__submission_is_deleted(datascience_bot_reddit, SubstantialStrain6_reddit):
    ## Create a post with u/SubstantialStrain6
    # fmt: off
    user_submission = (
        SubstantialStrain6_reddit
        .subreddit(display_name="datascience_bot_dev")
        .submit(
            title=f"Test datascience_bot:submission_is_removed | {TEST_TIME}",
            selftext="This is a test.",
            send_replies=False,
        )
    )
    # fmt: on

    # View u/SubstantialStrain6's post with u/datascience-bot
    mod = datascience_bot_reddit
    submission = update(user_submission, mod)

    assert submission_is_deleted(submission, mod) == False

    user_submission.delete()

    assert submission_is_deleted(submission, mod) == True


def test__submission_is_removed(datascience_bot_reddit, SubstantialStrain6_reddit):
    ## Create a post with u/SubstantialStrain6
    # fmt: off
    user_submission = (
        SubstantialStrain6_reddit
        .subreddit(display_name="datascience_bot_dev")
        .submit(
            title=f"Test datascience_bot:submission_is_removed | {TEST_TIME}",
            selftext="This is a test.",
            send_replies=False,
        )
    )
    # fmt: on

    # View u/SubstantialStrain6's post with u/datascience-bot
    mod = datascience_bot_reddit
    submission = update(user_submission, mod)

    assert submission_is_removed(submission, mod) == False

    submission.mod.remove(spam=False)

    assert submission_is_removed(submission, mod) == True


def test__get_datascience_bot():
    assert isinstance(get_datascience_bot(), praw.reddit.Reddit)


def test__get_SubstaintialStrain6():
    assert isinstance(get_SubstantialStrain6(), praw.reddit.Reddit)


def test__get_b3405920():
    assert isinstance(get_b3405920(), praw.reddit.Reddit)
