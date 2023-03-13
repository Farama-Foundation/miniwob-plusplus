# Viewing the Environments

There are 2 ways to view the environments:

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

