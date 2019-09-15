# -*- coding: utf-8 -*-
"""Common exceptions used in tasks
"""


class MissingSubmissionError(Exception):
    """When we can't find a particular submission."""


class InvalidTaskError(Exception):
    """When the task is invalid for on reason or another"""
