# -*- coding: utf-8 -*-
import json
import logging
import pathlib
from pprint import pprint
from typing import List, Tuple

import praw


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_opt_out_users() -> List[str]:
    """Get a list of opt-out users.

    We'll return a list instead of a generator because we need to load all
    the data to memory anyway.

    Returns:
        List[str]: The redditor IDs of users who've opted out
    """
    p = pathlib.Path("competition-data/opt-out-users.txt")

    return p.read_text().strip().split("\n")


def jsonify_submission(submission: praw.models.Submission) -> Tuple[str, dict]:
    """Convert a Reddit submission object to json

    Args:
        submission (praw.models.Submission): Submission to be converted

    Returns:
        Tuple[str, dict]: submission as json and as dict
    """
    d = submission.__dict__

    # The resulting dict key "author" will reference an unfetched Redditor
    # instance that is not json seralizable. We need to fetch it, and remove
    # unnecessary praw objects so we can convert the submission to json
    redditor = submission.author
    redditor.created_utc  # trigger fetch
    d["author"] = redditor.__dict__  # overwrite unfetched redditor instance

    # remove unnecessary Reddit objects that aren't JSON serializable
    d.pop("_reddit")
    d.pop("subreddit")
    d["author"].pop("_reddit")
    d["author"].pop("subreddit")

    return json.dumps(d), d


def save_submission(submission: praw.models.Submission) -> None:
    """Save submission as a json object in the competition-data dir

    Later we'll point the saved files to an S3 bucket.

    Args:
        submission (praw.models.Submission): Submission to be saved
    """
    opt_out_users = get_opt_out_users()
    if submission.author.id in opt_out_users:
        logger.warning(f"User {submission.author.id} has opted out of the competition")
        return None

    s, d = jsonify_submission(submission)

    # build path to data
    author_id = d["author"]["id"]
    submission_id = d["id"]

    fp = pathlib.Path(f"competition-data/data/{author_id}/{submission_id}.json")
    logger.info(f"Save data to {fp.resolve().as_posix()}")
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_bytes(s)


if __name__ == "__main__":
    import time

    reddit = praw.Reddit("SubstantialStrain6", user_agent="datascience-bot testing")
    subreddit = reddit.subreddit("datascience")

    for i, submission in enumerate(subreddit.new(limit=3)):
        if i > 0:
            time.sleep(0.5)
        save_submission(submission)
