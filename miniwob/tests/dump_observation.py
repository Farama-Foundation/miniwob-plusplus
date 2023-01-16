#!/usr/bin/env python
"""Dump the observation to stdout. Used for debugging."""
import argparse
import pprint

import gymnasium

import miniwob  # noqa: F401


def main():
    """Dump the observation to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", default=123, type=int, help="Seed")
    parser.add_argument(
        "-r",
        "--repeats",
        default=1,
        type=int,
        help="Repeat `reset` this number of times before printing",
    )
    parser.add_argument("env_name", help="Environment name")
    args = parser.parse_args()

    env = gymnasium.make(args.env_name)
    try:
        obs, info = env.reset(seed=args.seed)
        for _ in range(args.repeats - 1):
            obs, info = env.reset(seed=args.seed)
        pprint.pprint(obs)
        pprint.pprint(info)
    finally:
        env.close()


if __name__ == "__main__":
    main()
