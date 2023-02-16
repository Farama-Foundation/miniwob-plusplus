# Setup

## Install

Inside the repository directory, run

```
pip install .
```

If this gives you problems, try again and add pip's `--ignore-installed` flag.

## Selenium

* Outside this repository, download [ChromeDriver](https://chromedriver.chromium.org/downloads). Unzip it and then add the directory containing the `chromedriver` executable to the `PATH` environment variable

```
export PATH=$PATH:/path/to/chromedriver
```

* If instead you're using Anaconda, use

```
conda install -c conda-forge selenium
```

## Environment variable (optional)

One can set the shell variable `MINIWOB_BASE_URL` to point to the base URL of the benchmark. If the variable is not specified, the `file://` URL will be inferred from the module path.

* For the server setup:

```
export MINIWOB_BASE_URL=http://localhost:8080/
```

* For the file setup:
```
export MINIWOB_BASE_URL=file:///path/to/miniwob-plusplus/html/
```
