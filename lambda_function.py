#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""AWS Lambda entrypoint
"""
import logging
import sys
from typing import Dict

from tasks import post_weekly_thread, remove_spam


# config logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class EventConfigError(Exception):
    """When the event is not properly configured.

    The event must be a dict of two key-value pairs:
        "task": mapped to a str
        "kwargs": mapped to a dict
    """


class UnknownTaskError(Exception):
    """When the "task" value is not recognized or not supported

    The task should be named as the python file it intends to call.

    e.g. the following event would call the post_weekly_thread.handler:
    {
        "task": "post_weekly_thread",
        "kwargs": {}
    }
    """


def validate_event(event: Dict) -> None:
    """Validate the event dict passed to lambda_handler

    Args:
        event (Dict): AWS Lambda event payload

    Raises:
        EventConfigError: if event configuration is invalid
    """
    if not isinstance(event, dict):
        raise EventConfigError("AWS Lambda event must be a dict")
    if "task" not in event.keys():
        raise EventConfigError("AWS Lambda event is missing the `task` key")
    if not isinstance(event["task"], str):
        raise EventConfigError("AWS Lambda event 'task' key must map to a str")
    if "kwargs" not in event.keys():
        raise EventConfigError("AWS Lambda event is missing the `kwargs` key")
    if not isinstance(event["kwargs"], dict):
        raise EventConfigError("AWS Lambda event 'kwargs' key must map to a dict")


def lambda_handler(event: Dict, context) -> Dict:
    """Lambda function handler

    AWS Lambda Docs:
        https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html

    Args:
        event (Dict): See docs
        context

    Returns:
        Dict: Response to return to application
    """
    validate_event(event)

    task = event["task"]
    kwargs = event["kwargs"]

    if task == "post_weekly_thread":
        post_weekly_thread.main(**kwargs)
    elif task == "remove_spam":
        remove_spam.main(**kwargs)
    else:
        raise UnknownTaskError(f"The given task, '{task}', is not supported")


if __name__ == "__main__":
    lambda_handler(event={"task": "remove_spam", "kwargs": {}}, context=None)
