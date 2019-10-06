# -*- coding: utf-8 -*-
"""Update the wiki with data from datascience_bot/wiki/ dir
"""
import logging
import os
import pathlib
import sys

import praw

from datascience_bot import get_datascience_bot, add_boilerplate, __version__


# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")


def main():
    reddit = get_datascience_bot()
    subreddit = reddit.subreddit(SUBREDDIT_NAME)

    local_dir = (pathlib.Path(__file__).parent / ".." / "wiki").resolve()
    for f in local_dir.iterdir():
        page_name = f.stem
        if f.is_dir() or f.suffix != ".md":
            continue

        new_content = f.read_text()
        wiki_page = subreddit.wiki[page_name]
        wiki_page.edit(content=new_content, reason=f"Deploy version {__version__}")


if __name__ == "__main__":
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    if SUBREDDIT_NAME != "datascience_bot_dev":
        raise Exception("Test only against r/datascience_bot_dev!")

    main()
