# Action Space

An action is specified by an **action type** (e.g., `CLICK_COORDS`)
and the necessary fields for that action type (e.g., `coords=[30, 60]`).

## Supported Action Types

MiniWoB++ environments support the following action types:

```{list-table}
:header-rows: 1
* - Name
  - Description
* - `NONE`
  - Do nothing for the current step.
* - `MOVE_COORDS`
  - Move the cursor to the specified coordinates.
* - `CLICK_COORDS`
  - Click on the specified coordinates.
* - `DBLCLICK_COORDS`
  - Double-click on the specified coordinates.
* - `MOUSEDOWN_COORDS`
  - Start dragging on the specified coordinates.
* - `MOUSEUP_COORDS`
  - Stop dragging on the specified coordinates.
* - `SCROLL_UP_COORDS`
  - Scroll up on the mouse wheel at the specified coordinates.
* - `SCROLL_DOWN_COORDS`
  - Scroll down on the mouse wheel at the specified coordinates.
* - `CLICK_ELEMENT`
  - Click on the specified element.
* - `PRESS_KEY`
  - Press the specified [key or key combination](/content/key_combinations).
* - `TYPE_TEXT`
  - Type the specified string.
* - `TYPE_FIELD`
  - Type the value of the specified task field.
* - `FOCUS_ELEMENT_AND_TYPE_TEXT`
  - Click on the specified element, and then type the specified string.
* - `FOCUS_ELEMENT_AND_TYPE_FIELD`
  - Click on the specified element, and then type the value of the specified task field.
```

There are action types that perform similar actions (e.g., `CLICK_COORDS` and `CLICK_ELEMENT`).
A common practice is to specify a subset of action types that the agent can use in the config, as described below.

## Action Configs

The list of selected action types, along with other configurations, can be customized
by passing a `miniwob.action.ActionSpaceConfig` object to the `action_space_config` argument
during environment construction.

An `ActionSpaceConfig` object has the following fields:

```{list-table}
:header-rows: 1
* - Key
  - Type
  - Description
* - `action_types`
  - `Sequence[ActionTypes]`
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
* - `scroll_amount`
  - `int`
  - The amount to scroll for scroll actions.
* - `scroll_time`
  - `int`
  - Time in milliseconds to wait for scroll action animation.
* - `allowed_keys`
  - `Sequence[str]`
  - An ordered sequence of allowed [keys and key combinations](/content/key_combinations) for the `PRESS_KEY` action.
* - `text_max_len`
  - `int`
  - Maximum text length for the `TYPE_TEXT` action.
* - `text_charset`
  - `str` or `set[str]`
  - Character set for the `TYPE_TEXT` action.
```

## Action Object

The action passed to the [`step`](https://gymnasium.farama.org/api/env/#gymnasium.Env.step) method
should be a `dict` whose field inclusion depends on the selected action types:

```{list-table}
:header-rows: 1
* - Key
  - Type
  - Description
  - Inclusion
* - `action_type`
  - `int`
  - Action type index from the `action_types` list in the config.
  - Always.
* - `coords`
  - `np.ndarray` of shape `(2,)`
  - Left and top coordinates.
    Depending on the `coord_bins` config, the values can be of type `int8` (binned) or `float32` (unbinned).
  - When any `*COORDS` action type is selected.
* - `ref`
  - `int`
  - Element `ref` ID. If no element has the specified `ref`, the action becomes a no-op.
  - When any `*_ELEMENT*` action type is selected.
* - `key`
  - `int`
  - Key index from the `allowed_keys` list in the config.
  - When the `PRESS_KEY` action type is selected.
* - `text`
  - `str`
  - Text to type.
  - When any `*_TYPE_TEXT` action type is selected.
* - `field`
  - `int`
  - Index from the task field list `obs["fields"]`. If the index is out of bound, no text will be typed.
  - When any `*_TYPE_FIELD` action type is selected.
```

## Presets

The following preset names can be specified in place of the `ActionSpaceConfig` object:
(**TODO**: Implement this in code)

* `"all_supported"`: Select all supported actions, including redundant ones.
* `"shi17"`: The action space from (Shi et al., 2017)
  [World of Bits: An Open-Domain Platform for Web-Based Agents](http://proceedings.mlr.press/v70/shi17a/shi17a.pdf).
* `"liu18"`: The action space from (Liu et al., 2018)
  [Reinforcement Learning on Web Interfaces Using Workflow-Guided Exploration](https://arxiv.org/abs/1802.08802).
* `"humphreys22"`: The action space from (Humphreys et al., 2022)
  [A data-driven approach for learning to control computers](https://arxiv.org/abs/2202.08137).

