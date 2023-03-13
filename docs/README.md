# MiniWoB++ documentation

This directory contains the documentation for MiniWoB++.

For more information about how to contribute to the documentation go to our [CONTRIBUTING.md](https://github.com/Farama-Foundation/Celshast/blob/main/CONTRIBUTING.md)

## Build the Documentation

Install the required packages and Gymnasium (or your fork):

```
pip install -r docs/requirements.txt
pip install -e .
```

To generate the environment pages:

```
python docs/scripts/gen_mds.py
python docs/scripts/gen_env_list.py
```

To build the documentation once:

```
cd docs
sphinx-build . _build
```

To rebuild the documentation automatically every time a change is made:

```
pip install sphinx-autobuild
cd docs
sphinx-autobuild . _build
```
