# -*- coding: utf-8 -*-
from datetime import datetime
import os

import praw
import pytest

from datascience_bot import refresh_weekly_thread


TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


def test__refresh_weekly_thread():
    refresh_weekly_thread.main()
