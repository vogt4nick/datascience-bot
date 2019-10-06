# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import time

import praw
import pytest

from datascience_bot import get_datascience_bot, get_SubstantialStrain6, get_b3405920
from datascience_bot.cli import refresh_weekly_thread


TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


def test__refresh_weekly_thread():
    datascience_bot = get_datascience_bot()

    old_thread = refresh_weekly_thread.get_weekly_thread(datascience_bot)

    refresh_weekly_thread.main(validate=False)

    time.sleep(30)
    old_thread = datascience_bot.submission(id=old_thread.id)  # refresh cached version
    for comment in old_thread.comments:
        assert comment is not None
        assert len(comment.replies) > 0
