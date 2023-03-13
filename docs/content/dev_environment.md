# Development Environment

## Setup

To set up the environment for development:

* Follow the instructions in the [Python interface setup](/content/python_setup).

* Install test dependencies:
  ```sh
  pip install -e .[testing]
  ```

* Install git pre-commit hooks:
  ```sh
  pip install pre-commit
  pre-commit install
  ```

## Run Tests

At the root directory, run
```sh
pytest --timeout=20
```
This will run all tests in `tests/` with a timeout of 20 seconds per test.

