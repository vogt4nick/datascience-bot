# -*- coding: utf-8 -*-
"""Remove posts written by trolls or underqualified users
"""
import logging
import os
from typing import Coroutine

import praw


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
        logger.debug(
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
        weekly_thread_url = "https://www.reddit.com/r/datascience/search?q=Weekly%20Entering%20%26%20Transitioning%20Thread&restrict_sr=1&t=week"
        wiki_url = "https://www.reddit.com/r/datascience/wiki/index"
        message_the_mods_url = (
            "https://www.reddit.com/message/compose?to=%2Fr%2Fdatascience"
        )
        submission.reply(
            f"I removed your post to r/{submission.subreddit.display_name}.\n"
            "\n"
            f"r/{submission.subreddit.display_name} gets a lot of posts from "
            "new redditors. It's likely your topic or question has been "
            "discussed at length before, so we remove posts from authors with "
            f"less than 50 karma as a rule. You only have {total_karma} "
            "karma right now.\n"
            "\n"
            f"The [weekly entering & transitioning thread]({weekly_thread_url}) "
            "is a good place to start. You may also find useful resources on "
            f"[the wiki]({wiki_url}).\n"
            "\n"
            "If you believe this is an error, or you're intentionally posting "
            "with a throwaway account, please "
            f"[message the mods]({message_the_mods_url}) to approve your post."
        )
        submission.mod.remove(spam=False)

    logger.debug("Exit remove_troll_submission")


if __name__ == "__main__":
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
    if SUBREDDIT_NAME != "datascience_bot_dev":
        raise Exception("Test only against r/datascience_bot_dev!")

    reddit = praw.Reddit("datascience-bot", user_agent="datascience-bot")
    subreddit = reddit.subreddit(display_name=SUBREDDIT_NAME)

    for submission in subreddit.new(limit=100):
        remove_troll_submission(submission)
