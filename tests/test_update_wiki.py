# -*- coding: utf-8 -*-
from datetime import datetime
import os
import pathlib

import praw
import pytest

from datascience_bot.cli import update_wiki

TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


def test__update_wiki(datascience_bot_reddit):
    datascience_bot = datascience_bot_reddit

    local_wiki_dir = pathlib.Path(__file__).parent / ".." / "wiki"
    valid_wiki_pages = [p.stem for p in local_wiki_dir.iterdir()]

    for wiki_page in datascience_bot.subreddit(SUBREDDIT_NAME).wiki:
        if wiki_page.name not in valid_wiki_pages:
            continue

        test_content = f"Testing {TEST_TIME}"
        wiki_page.edit(content=test_content, reason=test_content)
        assert wiki_page.content_md == test_content

    update_wiki.main()

    for wiki_page in datascience_bot.subreddit(SUBREDDIT_NAME).wiki:
        if wiki_page.name in valid_wiki_pages:
            continue
        assert wiki_page.content_md != test_content
