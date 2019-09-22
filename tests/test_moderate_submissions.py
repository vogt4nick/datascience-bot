# -*- coding: utf-8 -*-
from datetime import datetime
import os
import random

import praw
import pytest

from datascience_bot.cli import moderate_submissions

TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


# ----------------------------------------------------------------------------
# Setup Test Posts
# ----------------------------------------------------------------------------
@pytest.fixture
def low_karma() -> praw.models.reddit.submission:
    reddit = praw.Reddit("SubstantialStrain6", user_agent="datascience-bot testing")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)
    submission = subreddit.submit(
        title=f"Test Low Karma | {TEST_TIME}",
        selftext="This is a test post.",
        send_replies=False,
    )

    return submission


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

    reddit = praw.Reddit("b3405920", user_agent="datascience-bot testing")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)
    submission = subreddit.submit(
        f"Test Video Spam | {TEST_TIME}", url=SPAM_VIDEO_URL, send_replies=False
    )

    return submission


# ----------------------------------------------------------------------------
# Run Tests
# ----------------------------------------------------------------------------
def test__moderate_submissions(low_karma, spam_video):
    moderate_submissions.main()


if __name__ == "__main__":
    low_karma()
    spam_video()
