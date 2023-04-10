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

### Observation Object

In all MiniWoB++ environments, an observation is a `dict` with the following fields:

```{list-table}
:header-rows: 1
* - Key
  - Type
  - Description
* - `utterance`
  - `str`
  - Task instruction string.
* - `fields`
  - `list[tuple[str, str]]`
  - Environment-specific key-value pairs extracted from the utterance;
    e.g., "Click on the OK button" → `[("target", "OK")]`.
    The fields are guaranteed to be the same during the same episode.
* - `screenshot`
  - `np.ndarray` with shape `(height, width, 3)` and type `uint8`
  - Screenshot as RGB values for each pixel. Note that some elements such as
    opened dropdown may not be captured in the screenshot.
* - `dom_elements`
  - `list[dict]`
  - List of feature dicts, each describing a DOM elements (see below).
```

### DOM Element Features

Each feature dict in `dom_elements` has the following fields:

```{list-table}
:header-rows: 1
* - Key
  - Type
  - Description
* - `ref`
  - `int`
  - Non-zero integer ID.
    * The `ref` for normal HTML elements start from 1.
    * Each HTML element retains the same `ref` during the same episode.
    * Non-empty text nodes are converted into pseudo-elements with `ref` counting down from -1.[^1]
* - `parent`
  - `int`
  - `ref` of the parent. For the root DOM element, `parent` will be 0.
* - `left`
  - `np.ndarray` with shape `(1,)` and type `float32`
  - Left coordinate relative to the screen (can be negative).
* - `top`
  - `np.ndarray` with shape `(1,)` and type `float32`
  - Top coordinate relative to the screen (can be negative).
* - `width`
  - `np.ndarray` with shape `(1,)` and type `float32`
  - Element width.
* - `height`
  - `np.ndarray` with shape `(1,)` and type `float32`
  - Element height.
* - `tag`
  - `str`
  - HTML tag.
    * For normal elements, this is the uppercased tag name (e.g., `"DIV"`).
    * For `<input>` elements, the input type is appended (e.g., `"INPUT_text"`).
    * Non-empty text nodes become pseudo-elements with tag `"t"`.[^1]
* - `text`
  - `str`
  - Text content, which is non-empty only for leaf elements.[^1]
* - `value`
  - `str`
  - Value of `<input>` element.
* - `id`
  - `str`
  - HTML `id` attribute.
* - `classes`
  - `str`
  - HTML `class` attribute (multiple classes are separated by spaces).
* - `bg_color`
  - `np.ndarray` with shape `(4,)` and type `float32`
  - Background color as RGBA value.
* - `fg_color`
  - `np.ndarray` with shape `(4,)` and type `float32`
  - Foreground color as RGBA value.
* - `flags`
  - `np.ndarray` with shape `(4,)` and type `int8`
  - Binary flags:
    * (`focused`) Whether the element is being focused on.
    * (`tampered`) Whether the element has been tampered (clicked, focused, typed, etc.).
    * (`targeted`) Whether the element is an event target (for recorded demonstrations).
    * (`is_leaf`) Whether the element is a leaf.
```

[^1]: **Note:** Regarding text nodes:
    * For an element with a single text node as its child (e.g., `<button>Submit</button>`),
      a text pseudo-element will not be created. The element will become a leaf with the
      `text` feature filled in.
    * For an element with a text node as one of its children (e.g., `<button>Submit <b>NOW</b></button>`),
      a text pseudo-element (negative `ref` and `tag = "t"`) will be created for the text node.

(action_space)=
## Action Space

### Supported Actions

MiniWoB++ environments support the following actions.

```{list-table}
:header-rows: 1
* - Name
  - Description
* - `NONE`
  - Do nothing for the current step.
* - `CLICK_COORDS`
  - Click on the specified coordinates.
* - `DBLCLICK_COORDS`
  - Double-click on the specified coordinates.
* - `MOUSEDOWN_COORDS`
  - Start dragging on the specified coordinates.
* - `MOUSEUP_COORDS`
  - Stop dragging on the specified coordinates.
* - `CLICK_ELEMENT`
  - Click on the specified element.
* - `DBLCLICK_ELEMENT`
  - Double-click on the specified element.
* - `MOUSEDOWN_ELEMENT`
  - Start dragging on the specified element.
* - `MOUSEUP_ELEMENT`
  - Stop dragging on the specified element.
* - `SCROLL_UP`
  - Scroll up on the mouse wheel.
* - `SCROLL_DOWN`
  - Scroll down on the mouse wheel.
* - `PRESS_KEY`
  - Press the specified key or key combination.
* - `TYPE_TEXT`
  - Type the specified string.
* - `TYPE_FIELD`
  - Type the value of the specified task field.
* - `FOCUS_ELEMENT_AND_TYPE_TEXT`
  - Click on the specified element, and then type the specified string.
* - `FOCUS_ELEMENT_AND_TYPE_FIELD`
  - Click on the specified element, and then type the value of the specified task field.
```

### Action Configs

The list of selected actions, along with other configurations, can be customized
by passing a `miniwob.action.ActionSpaceConfig` object to the `action_space_config` argument
during environment construction.
The `ActionSpaceConfig` object has the following fields:

```{list-table}
:header-rows: 1
* - Key
  - Type
  - Description
* - `action_types`
  - `Sequence[ActionTypes]` or `Sequence[str]`
  - An ordered sequence of action types to include.
* - `screen_width`
  - `float`
  - Screen width. Will be overridden by the environment constructor.
* - `screen_height`
  - `float`
  - Screen height. Will be overridden by the environment constructor.
* - `coord_bins`
  - `tuple[int, int]`
  - If specified, bin the x and y coordinates to these numbers of bins.
    Mouse actions will be executed at the middle of the specified partition.
* - `allowed_keys`
  - `Sequence[str]`
  - An ordered sequence of allowed keys and key combinations for the `PRESS_KEY` action.
* - `text_max_len`
  - `int`
  - Maximum text length for the `TYPE_TEXT` action.
* - `text_charset`
  - `str` or `set[str]`
  - Character set for the `TYPE_TEXT` action.
```

### Action Object

An action is a `dict` whose field inclusion depends on the selected actions:

```{list-table}
:header-rows: `
* - Key
  - Type
  - Description
* - `action_type`
  - `int`
  - Action type index from the `action_types` list in the config.
* - `coords`
  - `np.ndarray` of shape `(2,)`
  - Coordinates. Included when any `*COORDS` action is selected.
    Depending on the `coord_bins` config, `coords` can be of type `int8` (binned) or `float32` (unbinned).
* - `ref`
  - `int`
  - Element `ref` ID. Included when any `*_ELEMENT*` action is selected.
    If no element has the specified `ref`, the action becomes a no-op.
* - `key`
  - `int`
  - Key index from the `allowed_keys` list in the config.
    Included when the `PRESS_KEY` action is selected.
* - `text`
  - `str`
  - Text to type. Included when any `*_TYPE_TEXT` action is selected.
* - `field`
  - `int`
  - Task field index. Included when any `*_TYPE_FIELD` action is selected.
```

### Presets

The following preset names can be specified in place of the `ActionSpaceConfig` object:
(**TODO**: Implement this in code)

* `all_supported`: Select all supported actions, including redundant ones.
* `shi17`: The action space from (Shi et al., 2017)
  [World of Bits: An Open-Domain Platform for Web-Based Agents](http://proceedings.mlr.press/v70/shi17a/shi17a.pdf).
* `liu18`: The action space from (Liu et al., 2018)
  [Reinforcement Learning on Web Interfaces Using Workflow-Guided Exploration](https://arxiv.org/abs/1802.08802).
* `humphreys22`: The action space from (Humphreys et al., 2022)
  [A data-driven approach for learning to control computers](https://arxiv.org/abs/2202.08137).
