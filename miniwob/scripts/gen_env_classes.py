#!/usr/bin/env python
"""Generate environment classes and their docstrings."""
import argparse
import csv
import re
from typing import Mapping, Sequence

import gymnasium
from gymnasium.envs.registration import parse_env_id


CLASS_TEMPLATE = """
class {camel_name}Env(MiniWoBEnvironment):
    \"\"\"
    ## Description

    {desc}

    ## Example utterances

    {utterances}

    ## Utterance fields

    {fields}{notes}
    \"\"\"

    subdomain = "{name}"
"""


NOTES_TEMPLATE = """

    ## Additional notes

    {notes}"""


def _raw_env_name(env_id: str) -> str:
    """Convert ID like miniwob/click-test-v1 to click-test."""
    _, env_name, _ = parse_env_id(env_id)
    return env_name


def _camel_case(x: str) -> str:
    """Convert string to camel-case."""
    return re.sub(r"[-_ ]", "", x.title())


def _markdown_bullets(items: Sequence[str], indent=4) -> str:
    """Format the items as markdown bullets."""
    return "\n".join(" " * indent + "* " + x for x in items)


def print_class(
    env_id: str, desc: Mapping[str, str], seeds: Sequence[int], max_utterances: int = 5
):
    """Print the class for the environment.

    Args:
        env_id: Environment ID.
        desc: Environment description.
        seeds: List of seeds for sampling utterances.
        max_utterances: Maximum number of utterances to include.
    """
    # Sample initial states
    utterances = []
    fields = set()
    env = gymnasium.make(env_id)
    for seed in seeds:
        obs, info = env.reset(seed=seed)
        utt = obs["utterance"]
        if len(utterances) < max_utterances and utt not in utterances:
            utterances.append(utt)
        fields.update(x[0] for x in obs["fields"])
    env.close()
    # Collect additional notes
    notes = []
    if desc.get("Partial reward") not in (None, "none"):
        notes.append("**Partial reward:** " + desc["Partial reward"])
    if desc.get("Notes"):
        notes += desc["Notes"].split("\n")
    notes_section = ""
    if notes:
        notes_section = NOTES_TEMPLATE.format(notes=_markdown_bullets(notes).strip())
    # Print the class
    print(
        CLASS_TEMPLATE.format(
            camel_name=_camel_case(_raw_env_name(env_id)),
            desc=desc.get("Description", "TODO"),
            utterances=(_markdown_bullets(sorted(utterances)).strip() or "TODO"),
            fields=(_markdown_bullets(sorted(fields)).strip() or "(none)"),
            notes=notes_section,
            name=_raw_env_name(env_id),
        ).strip()
    )


def main():
    """Dump environment classes to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "-d",
        "--env-desc-csv",
        help="CSV file containing the environment info.",
    )
    parser.add_argument(
        "-s",
        "--num-seeds",
        type=int,
        default=20,
        help="Number of seeds to try for extracting environment info.",
    )
    parser.add_argument(
        "-u",
        "--max-utterances",
        type=int,
        default=5,
        help="Maximum number of example utterances in the docstring." "",
    )
    args = parser.parse_args()

    # Read environment descriptions from a CSV file.
    env_descs = {}
    if args.env_desc_csv:
        with open(args.env_desc_csv) as fin:
            for record in csv.DictReader(fin):
                env_descs[record["Name"]] = record

    # Get the list of all miniwob environments.
    envs = []
    for env_id, env_spec in gymnasium.registry.items():
        if env_spec.namespace == "miniwob":
            envs.append(env_id)
    envs.sort(key=lambda env_id: _raw_env_name(env_id))

    # Sample the environment.
    seeds = list(range(args.num_seeds))
    for env_id in envs:
        raw_env_id = _raw_env_name(env_id)
        if raw_env_id in env_descs:
            desc = env_descs[raw_env_id]
        else:
            desc = {}
        print_class(env_id, desc, seeds, args.max_utterances)
        # Separate by 2 newlines
        print()
        print()


if __name__ == "__main__":
    main()
