# Basic Usage

## Simple Example

The following code performs a deterministic action on the
[`click-test-2`](/environments/click-test-2) environment
(Instruction: Click button ONE.).

```python
import time
import gymnasium
from miniwob.action import ActionTypes

env = gymnasium.make('miniwob/click-test-2-v1', render_mode='human')

# Wrap the code in try-finally to ensure proper cleanup.
try:
  # Start a new episode.
  obs, info = env.reset()
  time.sleep(2)       # Only here to let you look at the environment.
  
  # Find the HTML element with text "ONE".
  for element in obs["dom_elements"]:
    if element["text"] == "ONE":
      break

  # Click on the element.
  action = env.action_space.sample()     # Template for the action.
  action["action_type"] = env.action_space_config.action_types.index(
      ActionTypes.CLICK_ELEMENT
  )
  action["ref"] = element["ref"]
  obs, reward, terminated, _, _ = env.step(action)

  # Check if the action was correct. 
  assert reward >= 0      # Should be around 0.8 since 2 seconds has passed.
  assert terminated is True
  time.sleep(2)

finally:
  env.close()
```

## Environment Initialization

```python
env = gymnasium.make('miniwob/click-test-2-v1', render_mode='human')
```

Common arguments include:

* `render_mode`: Render mode. Supported values are:
    - `None` (default): Headless Chrome, which does not show the browser window.
    - `'human'`: Show the browser window.
* `action_space_config`: Configuration for the action space.
  See the {ref}`action_space` section for details.
  Supported values are:
    - An `ActionSpaceConfig` object.
    - A preset name, which will instantiate an `ActionSpaceConfig` object.

(observation_space)=
## Observation Space

TODO: Add details

(action_space)=
## Action Space

TODO: Add details
