# Reward

In all environments, the reward is 0 during the episode, and a value in the range -1 to 1 (inclusive)
when the episode terminates.

## Reward processor

Originally, any positive reward is scaled by the remaining time on the timer.
Some environments also give partial rewards for partially correct answers
(see the documentation or docstring of each environment for details).

A **reward processor** can be used to returns custom rewards that ignore
the time penalty or partial rewards. A reward processor can be specified during
environment initialization:

```python
import gymnasium
from miniwob.reward import get_binary_reward

env = gymnasium.make('miniwob/ascending-numbers-v1', reward_processor=get_binary_reward)
```

The available reward processors include:

* `get_original_reward`: Returns the original reward. This is the default.
* `get_raw_reward`: Returns the raw reward without time penalty.
* `get_binary_reward`: Returns the binary reward without time penalty or partial reward. The terminal reward will be either -1 or 1. This is used in most previous publications.
* `get_thresholded_reward`: Returns the binary reward without time penalty or partial reward, but with any partial reward &geq; the specified threshold being treated as 1. This is needed for tasks that give continuous-valued partial rewards depending on how close the answer is to the correct answer. To specify this method as the reward processor, use `lambda metadata: get_thresholded_reward(metadata, threshold=VALUE)` or `functools.partial(get_thresholded_reward, threshold=VALUE)`.
