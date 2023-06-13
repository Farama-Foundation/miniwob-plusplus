"""HTTP server for serving environment HTMLs."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread


SERVER_SINGLETON = None


def start_http_server(html_dir: str):
    """Returns an HTTP server for serving environment HTMLs.

    Args:
        html_dir: Path to the html/ directory.

    Returns:
        Base URL that looks like "http://localhost:[port]/".
    """
    global SERVER_SINGLETON
    if SERVER_SINGLETON:
        httpd = SERVER_SINGLETON
    else:
        httpd = ThreadingHTTPServer(
            ("localhost", 0),
            functools.partial(SimpleHTTPRequestHandler, directory=html_dir),
        )

        def serve_forever(server):
            with server:
                server.serve_forever()

        thread = Thread(target=serve_forever, args=(httpd,))
        thread.daemon = True
        thread.start()
        SERVER_SINGLETON = httpd
    address, port = httpd.server_address
    return f"http://{address}:{port}/"
