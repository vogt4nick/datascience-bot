# -*- coding: utf-8 -*-
"""Remove posts written by trolls or underqualified users
"""
import logging
import os
from typing import Coroutine

import praw

from datascience_bot import add_boilerplate


logger = logging.getLogger(__name__)


def remove_troll_submission(submission: praw.models.reddit.submission) -> None:
    """Remove submission that posted by a troll or underqualified users.
    Reply with explanation or constructive advice if warranted.

    Args:
        submission (praw.models.reddit.submission): Submission to remove as
            troll or underqualified user.
    """
    logger.debug("Enter remove_troll_submission")

    redditor = submission.author
    if submission.approved:
        return None

    # check if user is a moderator first
    subreddit_moderators = list(submission.subreddit.moderator())
    if redditor in subreddit_moderators:
        logger.info(
            f"Submission {submission.id} was authored by an "
            f"r/{submission.subreddit.display_name} moderator, "
            f"u/{redditor.name}"
        )
        return None

    total_karma = redditor.link_karma + redditor.comment_karma

    if total_karma <= -10:
        submission.mod.remove(spam=True)
    if total_karma <= 50:
        # long urls
        weekly_thread = "[weekly entering & transitioning thread](https://www.reddit.com/r/datascience/search?q=Weekly%20Entering%20%26%20Transitioning%20Thread&restrict_sr=1&t=week)"
        the_wiki = "[the wiki](https://www.reddit.com/r/datascience/wiki/index)"
        message_the_mods = "[message the mods](https://www.reddit.com/message/compose?to=%2Fr%2Fdatascience)"

        text = add_boilerplate(
            f"I removed your submission to r/{submission.subreddit.display_name}.\n"
            f"\n"
            f"r/{submission.subreddit.display_name} gets a lot of posts from "
            f"new redditors. It's likely your topic or question has been "
            f"discussed at length before, so we remove posts from authors with "
            f"less than 50 karma as a rule. You only have {total_karma} "
            f"karma right now.\n"
            f"\n"
            f"The {weekly_thread} is a good place to start. You may also find "
            f"useful resources on {the_wiki}.\n"
            f"\n"
            f"If you believe this is an error, or you're intentionally posting "
            f"with a throwaway account, please {message_the_mods} to approve "
            f"your submission."
        )
        comment = submission.reply(text)
        comment.mod.distinguish(how="yes", sticky=True)

        submission.mod.remove(spam=False)

    logger.debug("Exit remove_troll_submission")


if __name__ == "__main__":
    from datascience_bot import get_datascience_bot

    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    if SUBREDDIT_NAME != "datascience_bot_dev":
        raise Exception("Test only against r/datascience_bot_dev!")

    reddit = get_datascience_bot()
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    for submission in subreddit.new(limit=100):
        remove_troll_submission(submission)
