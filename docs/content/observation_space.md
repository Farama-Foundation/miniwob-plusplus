# Observation Space

## Observation Object

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
  - Screenshot as RGB values for each pixel.
* - `dom_elements`
  - `list[dict]`
  - List of dicts, each listing properties of a *visible* DOM elements (see below).
```

## DOM Element Properties

Each dict in `dom_elements` has the following fields:

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
    * For normal elements, this is the lowercased tag name (e.g., `"div"`).
    * For `<input>` elements, the input type is appended (e.g., `"input_text"`).
    * Non-empty text nodes become pseudo-elements with tag `"t"`.[^1]
* - `text`
  - `str`
  - Text content, which is non-empty only for leaf elements.[^1]
* - `value`
  - `str`
  - HTML `value` attribute (for an `<input>` element).
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
      a text pseudo-element (negative `ref` and `tag = "t"`) will be created for each line of text
      in the text node.

