# -*- coding: utf-8 -*-
"""Markdown files as variables
"""
import pathlib


faq = (pathlib.Path(__file__).parent / "frequently-asked-questions.md").read_text()
index = (pathlib.Path(__file__).parent / "index.md").read_text()
resources = (pathlib.Path(__file__).parent / "resources.md").read_text()
