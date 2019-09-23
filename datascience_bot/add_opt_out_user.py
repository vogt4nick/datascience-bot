# -*- coding: utf-8 -*-
import logging

import praw

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def add_opt_out_user(redditor: praw.models.Redditor) -> None:
    """Add a user's ID to the list of opt-out users

    Args:
        redditor (praw.models.Redditor): User who has opted out
    """
