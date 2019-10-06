# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os

import praw
import pytest

from datascience_bot.cli import refresh_weekly_thread


TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


@pytest.fixture
def existing_thread(datascience_bot_reddit, SubstantialStrain6_reddit, b3405920_reddit):
    weekly_thread = datascience_bot_reddit.subreddit(SUBREDDIT_NAME).submit(
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
    SubstantialStrain6_reddit.submission(id=weekly_thread.id).reply(
        "I have a question that will go unanswered"
    )

    # make a comment and answer it
    comment = b3405920_reddit.submission(id=weekly_thread.id).reply(
        "I have a question that will be answered by SubstantialStrain6"
    )
    SubstantialStrain6_reddit.comment(id=comment.id).reply(
        "I'm answering your question"
    )

    return weekly_thread


def test__refresh_weekly_thread(existing_thread):
    unanswered_comments = []
    answered_comments = []
    for comment in existing_thread.comments:
        if len(comment.replies) == 0:
            unanswered_comments.append(comment)
        else:
            answered_comments.append(comment)

    refresh_weekly_thread.main()

    for comment in unanswered_comments:
        assert any(reply.author == "datascience-bot" for reply in comment.replies)
    for comment in answered_comments:
        assert all(reply.author != "datascience-bot" for reply in comment.replies)
