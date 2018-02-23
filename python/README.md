# Python Code for Interacting with MiniWoB++

## Setup

- Python dependencies
  ```
  pip install -r requirements.txt
  ```
  - If this gives you problems, try again and add pip's `--ignore-installed` flag.

- Selenium
  - Outside this repository, download
    [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    Unzip it and then add the directory
    containing the `chromedriver` executable to the `PATH` environment variable
    ```
    export PATH=$PATH:/path/to/chromedriver
    ```
  - If instead you're using Anaconda, use
    ```
    conda install -c conda-forge selenium
    ```

- Environment variable:
  The tests depend on the variable `MINIWOB_BASE_URL` to point to the base URL
  of the benchmark. Please see the main README on how to set up the tasks.
  - For the server setup:
    ```
    export MINIWOB_BASE_URL=http://localhost:8080/
    ```
  - For the file setup:
    ```
    export MINIWOB_BASE_URL=file:///path/to/miniwob-plusplus/html/
    ```
