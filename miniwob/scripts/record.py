#!/usr/bin/env python
"""A simple server for recording demonstrations.

Dependency: bottle
"""

import argparse
import base64
import gzip
import json
import os
import time
import zlib
from codecs import open
from typing import Any, Optional, Sequence

from bottle import Bottle, FormsDict, request, response


app = Bottle()


class Saver:
    """A manager for saving demonstrations."""

    outdir: Optional[str] = None

    def init_directory(self, outdir: str):
        """Set the directory to save demonstrations to."""
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        self.outdir = outdir

    def save(self, json_string: str) -> str:
        """Save the JSON-serialized data to disk and return the filename."""
        if self.outdir is None:
            raise ValueError("outdir is not initialized.")
        data = json.loads(json_string)
        task_name = data["taskName"]
        filename = (
            task_name + "_" + time.strftime("%m%d%H%M%S", time.gmtime()) + ".json"
        )
        filename = os.path.join(self.outdir, filename)
        while os.path.exists(filename):
            # Avoid collision
            filename += "x"
        with open(filename, "w") as fout:
            json.dump(data, fout)
        print(f"Saved to {filename}")
        return filename

    def save_turk(self, request_forms: FormsDict):
        """Save the data from a HTTP request to disk."""
        if self.outdir is None:
            raise ValueError("outdir is not initialized.")
        keys = [key for key in request_forms if key[0] == "d" and key[1:].isdigit()]
        for key in keys:
            data = Saver.decompress_turk(request_forms[key])
            filename = (
                "turk_" + time.strftime("%m%d%H%M%S", time.gmtime()) + key + ".json"
            )
            filename = os.path.join(self.outdir, filename)
            while os.path.exists(filename):
                # Avoid collision
                filename += "x"
            with open(filename, "wb") as fout:
                fout.write(data)  # type: ignore
            print(f"Saved to {filename}")

    @staticmethod
    def decompress_turk(compressed: str) -> bytes:
        """Decompress the data from a HTTP request."""
        data = base64.b64decode(compressed)
        data = zlib.decompress(data)
        return data

    def load(self, filename: str) -> Any:
        """Load the demonstration from a file."""
        if self.outdir is None:
            raise ValueError("outdir is not initialized.")
        opener = gzip.open if filename.endswith(".gz") else open
        with opener(os.path.join(self.outdir, filename)) as fin:
            return json.load(fin)

    def list_files(self) -> Sequence[str]:
        """Return the list of saved files."""
        if self.outdir is None:
            raise ValueError("outdir is not initialized.")
        return sorted(os.listdir(self.outdir))


saver = Saver()


@app.hook("after_request")
def enable_cors():
    """Enable the browser to request code from any origin."""
    # This is dangerous but whatever:
    response.headers["Access-Control-Allow-Origin"] = "*"


@app.post("/record")
def record():
    """Handle a POST request for recording a demonstration."""
    filename = saver.save(request.body.read())
    return f"saved to {filename}"


@app.post("/mturk/externalSubmit")
def turk():
    """Handle a POST request from Amazon Mechanical Turk."""
    saver.save_turk(request.forms)
    return "saved"


@app.get("/list")
def list_files():
    """Handle a GET request for listing all saved files."""
    return {"filenames": saver.list_files()}


@app.get("/view")
def view():
    """Handle a GET request for viewing a demonstration."""
    filename = request.query.filename
    return {"filename": filename, "episode": saver.load(request.query.filename)}


def main():
    """Start a Bottle server."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=8032, help="Open the connection at this port"
    )
    parser.add_argument("outdir", help="Directory to dump the demonstrations")
    parser.add_argument(
        "-g",
        "--global-access",
        action="store_true",
        help="Allow global access to the server",
    )
    args = parser.parse_args()

    saver.init_directory(args.outdir)

    # Start the server
    host = "localhost" if not args.global_access else "0.0.0.0"
    app.run(host=host, port=args.port)
    print("\nGood bye!")


if __name__ == "__main__":
    main()
