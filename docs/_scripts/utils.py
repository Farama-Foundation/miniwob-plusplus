"""Utilities for documentation generation."""
import logging

import gymnasium as gym


def get_all_registered_miniwob_envs():
    """Return all registered MiniWoB environments."""
    envs = []
    for env_spec in gym.registry.values():
        if env_spec.namespace == "miniwob":
            envs.append(env_spec)
    return sorted(envs, key=lambda x: x.name)


def trim_docstring(docstring):
    """Format whitespaces in the docstring."""
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = 232323
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < 232323:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return "\n".join(trimmed)


def extract_description_from_docstring(docstring):
    """Extract the task description for the docstring."""
    if not docstring:
        return ""
    lines = [line.strip() for line in docstring.splitlines() if line.strip()]
    if lines[0] != "## Description":
        logging.warning(f"Invalid docstring header: {lines[0]}")
        return ""
    return lines[1]
