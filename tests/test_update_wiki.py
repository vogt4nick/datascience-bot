# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime
import os
import pathlib

import praw
import pytest

from datascience_bot import __version__
from datascience_bot.cli import update_wiki

TEST_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
if SUBREDDIT_NAME != "datascience_bot_dev":
    raise Exception("Test only against r/datascience_bot_dev!")


def test__update_wiki(datascience_bot_reddit):
    from datascience_bot import wiki

    local_wiki_dir = pathlib.Path(wiki.__file__).parent

    local_wiki_content = defaultdict(
        str,
        {
            path.stem: path.read_text()
            for path in local_wiki_dir.iterdir()
            if not path.is_dir() and path.suffix == ".md"
        },
    )

    datascience_bot = datascience_bot_reddit
    for wiki_page in datascience_bot.subreddit(SUBREDDIT_NAME).wiki:
        if wiki_page.name in local_wiki_content:
            wiki_page.edit(content="", reason=f"Testing {__version__} at {TEST_TIME}")
            assert wiki_page.content_md == ""

    update_wiki.main()

    for wiki_page in datascience_bot.subreddit(SUBREDDIT_NAME).wiki:
        if wiki_page.name in local_wiki_content:
            # wiki content doesn't keep newlines at end of file, though we write them
            assert wiki_page.content_md == local_wiki_content[wiki_page.name].strip()
