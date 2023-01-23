# MiniWoB++

The MiniWoB++ benchmark is an extension of the [OpenAI MiniWoB benchmark](http://proceedings.mlr.press/v70/shi17a/shi17a.pdf).
It adds a number of tasks, Javascript interfaces, as well as
Python code for interacting with the environment via Selenium.

[The list of tasks can be viewed here](https://farama-foundation.github.io/miniwob-plusplus/)

[More statistics about the tasks](https://docs.google.com/spreadsheets/d/1fVJaBq9ShfwaUuukXNjYIMzCh3QBJPeW5WcLflzMC68)

The MiniWoB++ benchmark is introduced in our paper:

> **Reinforcement Learning on Web Interfaces using Workflow-Guided Exploration.**  
> _Evan Zheran Liu\*, Kelvin Guu\*, Panupong Pasupat\*, Tianlin Shi, Percy Liang_  
> ICLR, 2018.

Development on MiniWoB++ is currently ongoing to bring it up to our standards for mature projects (https://farama.org/project_standards.html) and will be maintained long term after this point. If you'd like to help out, you can join our discord server here- https://discord.gg/PfR7a79FpQ

---

# Viewing the Tasks

There are 2 ways to access the tasks:

* **Run a simple server:**

  * **Node.js:** Install and run `http-server` using
    ```
    npm install http-server -g      # Requires Node.js
    cd html/
    http-server
    ```
    The tasks should now be accessible at `http://localhost:8080/miniwob/`.

  * **Python:**
    ```
    python -m http.server 8080
    ```
    We found this method to be less stable with a large amount of access,
    which is required by reinforcement learning.

* **Use the `file://` protocol:** open `miniwob-plusplus/html/miniwob/` in the browser.
  * The URL should now be something like
  
        file:///path/to/miniwob-plusplus/html/miniwob/
              
  * This should show the directory listing of all task HTML files.

---

# Python Environment

The Python environment implements the
[Gymnasium](https://github.com/Farama-Foundation/Gymnasium/) interface.

## Setup

- Install the module
  - Inside the repository directory, run
    ```
    pip install .
    ```
  - If this gives you problems, try again and add pip's `--ignore-installed` flag.

- Selenium
  - Outside this repository, download
    [ChromeDriver](https://chromedriver.chromium.org/downloads).
    Unzip it and then add the directory
    containing the `chromedriver` executable to the `PATH` environment variable
    ```
    export PATH=$PATH:/path/to/chromedriver
    ```
  - If instead you're using Anaconda, use
    ```
    conda install -c conda-forge selenium
    ```

- Environment variable (optional):
  One can set the shell variable `MINIWOB_BASE_URL` to point to the base URL
  of the benchmark. If the variable is not specified, the `file://` URL will be
  inferred from the module path.
  - For the server setup:
    ```
    export MINIWOB_BASE_URL=http://localhost:8080/
    ```
  - For the file setup:
    ```
    export MINIWOB_BASE_URL=file:///path/to/miniwob-plusplus/html/
    ```

## Running Tests

```
pytest
```

The tests in the `miniwob/tests/` directory also illustrate how the code can be used.

---

# JavaScript Utilities

This version of MiniWoB environments incorporates a few JavaScript utilities,
many of which are used by the Python interface.

## `Math.seedrandom([seed])`

Set the global random seed of the environment. The optional argument `seed` can be an object.

## `getDOMInfo()`

Returns a nested object containing information about the current DOM states.
The returned object corresponds to the `<body>` element. Its children can be accessed under the `children` field.

In Python, the `step` method in `MiniWoBInstance` calls this function to build the `MiniWoBState`.

### Output Format

Each visible DOM element is converted into an object with the following fields:

* `tag` (string): Tag name
  * For normal elements, this is the uppercased tag name (e.g., `"DIV"`)
  * For `<input>` elements, the input type is appended (e.g., `"INPUT_text"`)
  * Each non-empty text node is converted into pseudo-elements with tag `"t"`,
    where each pseudo-element represents one line of text.
    However, if the text node is the only child of the parent. The text pseudo-element is not created,
    and its text is assigned to the parent element instead.
* `ref` (number): Reference number
  * Within each episode, the `ref` number of the same object stays the same
  * For the same random seed, the `ref` number of the same object should be the same
  * `ref` for normal elements start from 1, while `ref` for text psuedo-elements counts down from -1
* `children` (list): Recursive list of objects corresponding to the children
* `left`, `top`, `width`, `height` (number): Geometry of the element
* `id` (string): Element's `id`
* `classes` (string): Element's `class`es (space-separated)
* `bgColor`, `fgColor` (string): Background and foreground colors
* `focused` (boolean): Indicates if the element is being focused on
* `tampered` (boolean): Indicates if the element is tampered (clicked, focused, typed, etc.)
* `value`: For `<input>`, this contains the input value
  * For `checkbox` and `radio` types, this contains a boolean whether the input is selected
  * For other input types, this contains a text value
* `text` (string): For child nodes and text pseudo-elements, this contains the text content

## `flattenDOMInfo(rootDomInfo)`

Can be called on the result of `getDOMInfo()` to get a flattened representation.
Useful for debugging in Chrome console.

## `elementClick(ref)`

Click on an element regardless of its location and visibility.
The argument `ref` is the ref value generated by the previous call to `getDOMInfo()`.

## `visualizeAttention(values)`

Visualize the attention weights on the screen.
The argument `values` is a 2D array of shape 20 × 20.

---
    
# Demonstrations

We have recorded demonstrations from Mechanical Turk and put them in a [separate repository](https://github.com/stanfordnlp/miniwob-plusplus-demos).

## Demonstration Format

Each demonstration is saved as a JSON file. The root object generated by `core/record.js` contains the following fields:

* `taskName` (string)
* `utterance` (string)
* `reward` (number): Reward as defined by the task
* `rawReward` (number): 1 if succeeded and -1 if failed
* `states`: a list of state objects
  * One state is recorded for the initial state
  * Two states are recorded for each event, one before the event resolves and one after the event resolves

Each state object has the following fields:

* `time` (number): Time elapsed since the episode started
* `action`: An action-specific object (not present for the initial state) with the following common keys:
  * `type` (string)
  * `timing` (number): the `eventPhase` property of the JS event object.
    This is 1 before the event resolves (capturing state) and 3 after the event resolves (bubbling state).
* `dom`: The DOM info as generated by `getDOMInfo()`
  * The event target will have a special key `recordingTarget` set to `true`.

## Recording Your Own Demonstrations

1. Start the recording server:
   ```
   # Create an output directory
   mkdir out/
   python -m miniwob.record out/
   ```

2. Append `?record=true` to the URL of the task you want to record. For example, for the `click-test` task, go to
   ```
   file:///path/to/miniwob-plusplus/html/miniwob/click-test.html?record=true
   ```
   (Note: For recent versions of Chrome, you might have to retype the whole URL instead of just appending `?record=true`.)

3. To view the results, open `viewer/viewer.html` while the recording server is running. The URL should be like
   ```
   file:///path/to/miniwob-plusplus/html/viewer/viewer.html
   ```
