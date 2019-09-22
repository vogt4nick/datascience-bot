# -*- coding: utf-8 -*-
"""datascience-bot helps moderate r/datascience on Reddit
"""
import praw

__author__ = "vogt4nick"
__copyright__ = "Copyright 2019, Nick Vogt"
__license__ = "MIT"
__version__ = "2019.9.22.dev3"
__maintainer__ = "vogt4nick"
__email__ = "vogt4nick@gmail.com"
__status__ = "Production"


def update(target, reddit: praw.models.reddit):
    """Update the target object using the given reddit instance

    Args:
        target ([type]): one of subreddit, submission, or comment
        reddit (praw.models.reddit): the reddit session used to refresh
            the target object

    Returns:
        praw.models.Subreddit: if target is a subreddit
        praw.models.Submission: if target is a submission
        praw.models.Comment: if target is a comment
    """
    if isinstance(target, praw.models.Subreddit):
        subreddit = target
        return reddit.subreddit(display_name=subreddit.display_name)

    if isinstance(target, praw.models.Submission):
        submission = target
        return reddit.submission(id=submission.id)

    if isinstance(target, praw.models.Comment):
        comment = target
        return reddit.comment(id=comment.id)

    raise Exception(
        "`target` must be one of (subreddit, submission, comment). "
        f"Not {type(target)}"
    )


def submission_is_deleted(
    submission: praw.models.Submission, reddit: praw.models.reddit
) -> bool:
    """Returns true if the given submission has been deleted by the author

    Args:
        submission (praw.models.Submission): Submission to test
        reddit (praw.models.reddit): reddit instance used to refresh submission

    Returns:
        bool: True if the submission has been deleted. Else False.
    """
    submission = update(submission, reddit)

    # modified code from following source:
    # https://www.reddit.com/r/redditdev/comments/44a7xm/praw_how_to_tell_if_a_submission_has_been_removed/czoreie
    if submission.author is None:
        if submission.selftext == "[deleted]":
            return True
        if submission.selftext == "[removed]":
            return True
        return True
    if submission.selftext == "[removed]":
        return True

    return False


def submission_is_removed(
    submission: praw.models.Submission, reddit: praw.models.reddit
) -> bool:
    """Returns true if the given submission has been removed by a moderator

    Args:
        submission (praw.models.Submission): Submission to test
        reddit (praw.models.reddit): reddit instance used to refresh submission

    Returns:
        bool: True if the submission has been removed. Else False.
    """
    submission = update(submission, reddit)

    # spam posts are removed, but don't trigger the submission.removed flag
    # https://www.reddit.com/r/redditdev/comments/d3vqix/how_to_check_if_a_submission_has_been_removed_as/
    return submission.spam or submission.removed
