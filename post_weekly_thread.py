# -*- coding: utf-8 -*-
# fmt: off
# For whatever reason, black is unable to format this file as of v19.3b
# We must disable it for now. :/
"""Post the weekly entering & transitioning thread to r/datascience using
u/datascience-bot.
"""
from datetime import datetime, timedelta
import logging
import pathlib
import requests
from typing import Tuple

import praw


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MissingSubmissionError(Exception):
    """When we can't find a particular submission."""


def get_weekly_thread_dates() -> Tuple[str]:
    """Get dates to replace values in templates/weekly-thread/title.txt

    Should span one week; i.e. Sunday - Sunday.

    Returns:
        Tuple[str]: Tuple of formatted start_date and end_date.
    """
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=7)

    time_template = "%d %b %Y"
    formatted_start_date = start_date.strftime(time_template)
    formatted_end_date = end_date.strftime(time_template)

    return formatted_start_date, formatted_end_date


def get_weekly_thread_title() -> str:
    """Get the weekly thread's title from file and format with proper dates

    Returns:
        str: Formatted thread title
    """
    start_date, end_date = get_weekly_thread_dates()
    title_template = pathlib.Path("./templates/weekly-thread/title.md").read_text()

    # fmt: off
    title = (
        title_template.replace("{{start_date}}", start_date)
        .replace("{{end_date}}", end_date)
        .strip()
    )

    return title


def get_weekly_thread_selftext() -> str:
    """Get the weekly thread's selftext from file

    Returns:
        str: Weekly thread's selftext
    """
    # fmt: off
    selftext = (
        pathlib.Path("./templates/weekly-thread/selftext.md")
        .read_text()
        .strip()
    )
    return selftext


def post_weekly_thread(r_datascience: praw.models.reddit.subreddit) -> None:
    """Post the weekly thread with required attributes

    Args:
        r_datascience (praw.models.reddit.subreddit): r/datascience subreddit
    """
    title = get_weekly_thread_title()
    selftext = get_weekly_thread_selftext()
    submission = r_datascience.submit(
        title=title,
        selftext=selftext,
        send_replies=False,
    )
    # Set thread attributes
    submission.mod.flair(text="Discussion")
    submission.mod.approve()
    submission.mod.distinguish()
    submission.mod.sticky(state=True, bottom=True)


def remove_last_sticky(datascience_bot: praw.models.reddit.redditor) -> None:
    """Remove the last thread stickied by u/datascience-bot

    Args:
        datascience_bot (praw.models.reddit.redditor): u/datascience-bot user
    """
    for submission in datascience_bot.new(limit=100):
        if submission.stickied:
            submission.mod.sticky(state=False)
            return None
    else:
        raise MissingSubmissionError("Could not find the last stickied thread")


def main():
    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    r_datascience = reddit.subreddit("datascience")
    datascience_bot = reddit.redditor(name="datascience-bot")

    try:
        remove_last_sticky(datascience_bot)
    except MissingSubmissionError:
        # just warn about this error until we're fully operational
        logging.warning("Unable to find last submission")

    post_weekly_thread(r_datascience)


if __name__ == "__main__":
    main()
