# -*- coding: utf-8 -*-
"""Post the weekly entering & transitioning thread to r/datascience using
u/datascience-bot.
"""
from datetime import datetime, timedelta
import logging
import os
import sys
from typing import Dict, Tuple

import praw

# config logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class MissingSubmissionError(Exception):
    """When we can't find a particular submission."""


class InvalidTaskError(Exception):
    """When the task is invalid for on reason or another"""


def get_last_weekly_thread(
    subreddit: praw.models.reddit.subreddit
) -> praw.models.reddit.submission:
    """Get the last weekly thread created by u/datascience-bot

    Args:
        subreddit (praw.models.reddit.subreddit): Subreddit to search for last
            weekly thread

    Returns:
        praw.models.reddit.submission: Last stickied thread in the given
            subreddit posted by u/datascience-bot titled as
            "Weekly Entering & Transitioning Thread"

    Raises:
        MissingSubmissionError: When last weekly thread can't be found
    """
    for submission in subreddit.hot(limit=2):  # max 2 possible stickies
        if (
            submission.subreddit == subreddit
            and submission.title.startswith("Weekly Entering & Transitioning Thread")
            and submission.stickied
            and submission.author == "datascience-bot"
        ):
            logger.info(
                f"Found old weekly thread: {submission.id}; "
                f"reddit.com{submission.permalink}"
            )
            return submission
    else:
        raise MissingSubmissionError("Could not find the last stickied thread")


def validate_task(subreddit: praw.models.reddit.subreddit) -> None:
    """Validate whether it's appropriate to run the task right now

    Args:
        subreddit (praw.models.reddit.subreddit): which subreddit to validate
            task against.

    Raise:
        InvalidTaskError: When it's not Sunday UTC time or the current weekly
            thread is under 1 day old
    """
    logger.info("Validate post_weekly_thread task")

    # test if its Sunday
    now = datetime.utcnow()
    if now.strftime("%A") != "Sunday":
        msg = (
            "This post_weekly_thread task is invalid. "
            "post_weekly_thread must be run on Sundays UTC time. "
            f"Right now it's {now.strftime('%A')} UTC time."
        )
        raise InvalidTaskError(msg)

    # get the last thread to determine when it was posted
    try:
        last_weekly_thread = get_last_weekly_thread(subreddit)
    except MissingSubmissionError as err:
        # warn and raise no error
        logger.warning(err)
        pass
    else:
        # test if the last weekly thread is less than 24 hours old
        end_date_str = last_weekly_thread.title[55:]
        end_date = datetime.strptime(end_date_str, "%d %b %Y")
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if end_date > today:
            msg = (
                "This post_weekly_thread task is invalid. "
                "The last weekly thread cannot be replaced until "
                f"{end_date.strftime('%d %b %Y')}."
            )
            raise InvalidTaskError(msg)


def unsticky_last_weekly_thread(subreddit: praw.models.reddit.subreddit) -> None:
    """Unsticky the last weekly entering & transitioning thread

    Args:
        subreddit (praw.models.reddit.subreddit): which subreddit to search
            for sticky
    """
    logger.info("Remove last weekly entering & transitioning thread")

    last_weekly_thread = get_last_weekly_thread(subreddit)
    last_weekly_thread.mod.sticky(state=False)

    logger.debug("Successfully removed last sticky thread posted by u/datascience-bot")


def post_weekly_thread(subreddit: praw.models.reddit.subreddit) -> None:
    """Post the weekly thread with required attributes

    Args:
        subreddit (praw.models.reddit.subreddit): which subreddit to post
            weekly thread
    """
    logger.info("Post weekly entering & transitioning thread")

    # e.g. Weekly Entering & Transitioning Thread | 15 Sep 2019 - 22 Sep 2019
    title = (
        "Weekly Entering & Transitioning Thread | "
        f"{datetime.utcnow().strftime('%d %b %Y')} - "
        f"{(datetime.utcnow() + timedelta(days=7)).strftime('%d %b %Y')}"
    ).strip()

    # Long URLs we'll use to format the selftext
    faq_url = "https://www.reddit.com/r/datascience/wiki/frequently-asked-questions"
    resources_url = "https://www.reddit.com/r/datascience/wiki/resources"
    past_threads_url = "https://www.reddit.com/r/datascience/search?q=weekly%20thread&restrict_sr=1&t=month"

    selftext = (
        "Welcome to this week's entering & transitioning thread! "
        "This thread is for any questions about getting started, studying, or "
        "transitioning into the data science field. Topics include:\n"
        "\n"
        "* Learning resources (e.g. books, tutorials, videos)\n"
        "* Traditional education (e.g. schools, degrees, electives)\n"
        "* Alternative education (e.g. online courses, bootcamps)\n"
        "* Job search questions (e.g. resumes, applying, career prospects)\n"
        "* Elementary questions (e.g. where to start, what next)\n"
        "\n"
        "While you wait for answers from the community, check out the "
        f"[FAQ]({faq_url}) and [Resources]({resources_url}) pages on our wiki.\n"
        "\n"
        f"[You can also search for past weekly threads here]({past_threads_url}).\n"
        "\n"
        f"^(Posted at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')} UTC)"
    )
    submission = subreddit.submit(title=title, selftext=selftext, send_replies=False)
    # Set thread attributes
    submission.mod.flair(text="Discussion")
    submission.mod.approve()
    submission.mod.distinguish()
    submission.mod.sticky(state=True, bottom=True)

    logger.debug("Successfully posted weekly entering & transitioning thread")


def main():
    """Refresh the weekly thread
    """
    logger.info("Enter post_weekly_thread.main.py")

    # either datascience_bot_dev for testing, or datascience for production
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    logger.info(f"Acting on subreddit: {subreddit.display_name}")

    try:
        validate_task(subreddit)  # raises error if not valid
    except InvalidTaskError as err:
        logger.info(err)
        logger.info("Exit post_weekly_thread.main.py")
        return None

    try:
        unsticky_last_weekly_thread(subreddit)
    except MissingSubmissionError:
        # just warn about this error until we're fully operational
        logger.warning("Unable to find last submission")

    post_weekly_thread(subreddit)

    logger.info("Exit post_weekly_thread.main.py")


if __name__ == "__main__":
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    if SUBREDDIT_NAME != "datascience_bot_dev":
        raise Exception("Test only against r/datascience_bot_dev!")

    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    main()
