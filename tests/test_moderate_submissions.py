# -*- coding: utf-8 -*-
from datetime import datetime
import os
import random
import time

import praw
import pytest

from datascience_bot import (
    update,
    submission_is_deleted,
    submission_is_removed,
    get_datascience_bot,
    get_b3405920,
    get_SubstantialStrain6,
)
from datascience_bot.cli import moderate_submissions

TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


# ----------------------------------------------------------------------------
# Setup Test Posts
# ----------------------------------------------------------------------------


@pytest.fixture
def spam_video() -> praw.models.reddit.submission:
    """Post a spam video for datascience-bot to remove

    Returns:
        praw.models.reddit.submission: The spam submission
    """
    # If we post the same video over and over again, Reddit automatically flags it
    # as spam. So let's pick a random video from this list.
    # fmt: off
    SPAM_VIDEO_URL = random.choice([
        "https://www.youtube.com/watch?reload=9&v=-SD9DkKyOrY",  # Drum beat
        "https://www.youtube.com/watch?v=ewGAmiLuYCw",  # Jumping into Mousetraps
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Never Gonna Give You Up
        "https://www.youtube.com/watch?v=-qstIEHDVRg",  # 80s Gotye
    ])
    # fmt: on

    reddit = get_b3405920()
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)
    submission = subreddit.submit(
        f"Test Video Spam | {TEST_TIME}", url=SPAM_VIDEO_URL, send_replies=False
    )

    return submission


@pytest.fixture
def low_karma() -> praw.models.reddit.submission:
    reddit = get_SubstantialStrain6()
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)
    submission = subreddit.submit(
        title=f"Test Low Karma | {TEST_TIME}",
        selftext="This is a test post.",
        send_replies=False,
    )

    return submission


# ----------------------------------------------------------------------------
# Run Tests
# ----------------------------------------------------------------------------
def test__moderate_spam(spam_video):
    reddit = get_datascience_bot()
    submission = update(spam_video, reddit)

    assert submission_is_removed(submission, reddit) == False

    moderate_submissions.main()

    assert submission_is_removed(submission, reddit) == True
    assert submission.spam == True


def test__moderate_low_karma(low_karma):
    reddit = get_datascience_bot()
    mod_view = update(low_karma, reddit)

    assert submission_is_removed(mod_view, reddit) == False

    moderate_submissions.main()

    assert submission_is_removed(mod_view, reddit) == True


if __name__ == "__main__":
    low_karma()
    spam_video()
