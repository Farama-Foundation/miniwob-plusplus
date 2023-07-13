#!/usr/bin/env python
"""Dump the observation to stdout. Used for debugging."""
import argparse
import pprint

import gymnasium


def check_obs(obs, env):
    """Check if the observation is in the observation space."""
    obs_space = env.observation_space
    if obs in obs_space:
        return
    # Debug observation outside the space.
    if obs["utterance"] not in obs_space["utterance"]:
        print("BAD utterance: {}".format(obs["utterance"]))
    if obs["screenshot"] not in obs_space["screenshot"]:
        print("BAD screenshot: {}".format(obs["screenshot"]))
    if obs["fields"] not in obs_space["fields"]:
        print("BAD fields: {}".format(obs["fields"]))
    elt_space = obs_space["dom_elements"].feature_space
    for i, elt in enumerate(obs["dom_elements"]):
        if elt not in elt_space:
            print(f"BAD element {i}: {elt}")
            for key in elt_space:
                if elt[key] not in elt_space[key]:
                    print(f"... at key {key}: {elt[key]}")


def main():
    """Dump the observation to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument("env_name", help="Environment name")
    parser.add_argument("-s", "--seed", default=123, type=int, help="Seed")
    parser.add_argument(
        "-e", "--num_episodes", default=1, type=int, help="Number of episodes"
    )
    parser.add_argument(
        "-o",
        "--episode_offset",
        default=0,
        type=int,
        help="Run reset() this number of times before dumping",
    )
    parser.add_argument(
        "-a",
        "--num_actions",
        default=0,
        type=int,
        help="Number of random actions to perform on each episode",
    )
    args = parser.parse_args()

    env = gymnasium.make(args.env_name)
    try:
        for _ in range(args.episode_offset):
            env.reset(seed=args.seed)
        for i in range(args.num_episodes):
            print(f"===== Episode {i} =====")
            obs, info = env.reset(seed=args.seed)
            pprint.pprint(obs)
            check_obs(obs, env)
            pprint.pprint(info)
            print()
            for j in range(args.num_actions):
                print(f"----- Action {j} -----")
                action = env.action_space.sample()
                obs, reward, terminated, truncated, info = env.step(action)
                pprint.pprint(action)
                pprint.pprint(obs)
                check_obs(obs, env)
                print(f"Reward: {reward}, Terminated: {terminated}")
                pprint.pprint(info)
                print()
                if terminated:
                    break
    finally:
        env.close()


if __name__ == "__main__":
    main()
