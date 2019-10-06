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

from datascience_bot import get_datascience_bot, add_boilerplate

# config logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")


class MissingSubmissionError(Exception):
    """When we can't find a particular submission."""


class InvalidTaskError(Exception):
    """When the task is invalid for on reason or another"""


def get_weekly_thread(
    reddit: praw.models.reddit.subreddit
) -> praw.models.reddit.submission:
    """Get the last weekly thread created by u/datascience-bot

    Args:
        reddit (praw.models.reddit): Which reddit to search for last
            weekly thread with

    Returns:
        praw.models.reddit.submission: Last stickied thread in the given
            subreddit posted by u/datascience-bot titled as
            "Weekly Entering & Transitioning Thread"

    Raises:
        MissingSubmissionError: When last weekly thread can't be found
    """
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
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


def validate_task(reddit: praw.models.reddit) -> None:
    """Validate whether it's appropriate to run the task right now

    Args:
        reddit (praw.models.reddit): which reddit to validate task with

    Raise:
        InvalidTaskError: When it's not Sunday UTC time or the current weekly
            thread is under 1 day old
    """
    logger.info("Validate post_weekly_thread task")

    # test if its Sunday
    now = datetime.utcnow()
    if now.strftime("%A") != "Sunday":
        raise InvalidTaskError(
            "This post_weekly_thread task is invalid. "
            "post_weekly_thread must be run on Sundays UTC time. "
            f"Right now it's {now.strftime('%A')} UTC time."
        )

    # get the last thread to determine when it was posted
    try:
        last_weekly_thread = get_weekly_thread(reddit)
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


def unsticky_weekly_thread(reddit: praw.models.reddit) -> praw.models.Submission:
    """Unsticky the last weekly entering & transitioning thread

    Args:
        reddit (praw.models.reddit): which reddit to search for sticky

    Return:
        praw.models.Submission: Now unstickied weekly thread
    """
    logger.info("Remove last weekly entering & transitioning thread")

    last_weekly_thread = get_weekly_thread(reddit)
    last_weekly_thread.mod.sticky(state=False)

    return last_weekly_thread


def post_weekly_thread(reddit: praw.models.reddit) -> praw.models.Submission:
    """Post the weekly thread with required attributes

    `post_weekly_thread` does three things:
        1. Create the submission title and selftext
        2. Post the submission
        3. Distinguish, sticky, flair, etc.

    Args:
        reddit (praw.models.reddit): which reddit to post weekly thread

    Return:
        praw.models.Submission: New weekly thread
    """
    logger.info("Post weekly entering & transitioning thread")

    ## 1. Create the submission title and selftext
    # e.g. Weekly Entering & Transitioning Thread | 15 Sep 2019 - 22 Sep 2019
    title = (
        "Weekly Entering & Transitioning Thread | "
        f"{datetime.utcnow().strftime('%d %b %Y')} - "
        f"{(datetime.utcnow() + timedelta(days=7)).strftime('%d %b %Y')}"
    ).strip()

    # Long URLs we'll use to format the selftext
    faq = "[FAQ](https://www.reddit.com/r/datascience/wiki/frequently-asked-questions)"
    resources = "[Resources](https://www.reddit.com/r/datascience/wiki/resources)"
    past_weekly_threads = "[past weekly threads](https://www.reddit.com/r/datascience/search?q=weekly%20thread&restrict_sr=1&sort=new)"

    selftext = add_boilerplate(
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
        f"While you wait for answers from the community, check out the {faq} "
        f"and {resources} pages on our wiki. You can also search for "
        f"{past_weekly_threads}."
    )

    ## 2. Post the submission
    submission = reddit.subreddit(SUBREDDIT_NAME).submit(
        title=title, selftext=selftext, send_replies=False
    )

    ## 3. Distinguish, sticky, flair, etc.
    submission.mod.flair(text="Discussion")
    submission.mod.approve()
    submission.mod.distinguish()
    submission.mod.sticky(state=True, bottom=True)

    return submission


def direct_unanswered_comments_to_weekly_thread(
    reddit: praw.models.reddit, old_thread_id: str, new_thread_id: str
) -> None:
    """Direct unanswered comments in last weekly thread to the new weekly thread

    Args:
        reddit (praw.models.reddit): Reddit account to comment with
        old_thread_id (str)
        new_thread_id (str)
    """
    old_thread = reddit.submission(id=old_thread_id)
    new_thread = reddit.submission(id=new_thread_id)

    new_weekly_thread_md = f"[new weekly thread]({new_thread.permalink})"
    msg = add_boilerplate(
        f"I created a {new_weekly_thread_md}. Since you didn't receive any "
        "replies here, please feel free to resubmit your comment in the new "
        "thread.\n\n"
        "Thanks."
    )

    for comment in old_thread.comments:
        if len(comment.replies) == 0:
            reply = comment.reply(msg)
            reply.mod.distinguish(how="yes")


def main():
    """Refresh the weekly thread
    """
    logger.info("Enter post_weekly_thread.main.py")

    # either datascience_bot_dev for testing, or datascience for production
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    reddit = get_datascience_bot()
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    logger.info(f"Acting on subreddit: {subreddit.display_name}")

    validate_task(reddit)  # raises error if not valid
    old_thread = unsticky_weekly_thread(reddit)
    new_thread = post_weekly_thread(reddit)

    direct_unanswered_comments_to_weekly_thread(
        reddit, old_thread_id=old_thread.id, new_thread_id=new_thread.id
    )


if __name__ == "__main__":
    if SUBREDDIT_NAME != "datascience_bot_dev":
        raise Exception("Test only against r/datascience_bot_dev!")

    main()
