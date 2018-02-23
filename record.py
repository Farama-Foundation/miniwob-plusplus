#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple server for recording demonstrations.

Dependency: bottle
"""

import sys, os, shutil, re, argparse, json, time
from codecs import open
from itertools import izip
from collections import defaultdict, Counter

from bottle import Bottle, request, response
app = Bottle()

import base64, zlib, gzip

class Saver(object):
    outdir = None

    def init_directory(self, outdir):
        assert os.path.isdir(outdir), '{} is not a directory'.format(outdir)
        self.outdir = outdir

    def save(self, data):
        data = json.loads(data)
        task_name = data['taskName']
        filename = (task_name + '_' + 
                time.strftime('%m%d%H%M%S', time.gmtime()) + '.json')
        filename = os.path.join(self.outdir, filename)
        while os.path.exists(filename):
            # Avoid collision
            filename += 'x'
        with open(filename, 'w') as fout:
            json.dump(data, fout)
        print 'Saved to {}'.format(filename)
        return filename

    def save_turk(self, request):
        keys = [key for key in request.forms if key[0] == 'd' and key[1:].isdigit()]
        for key in keys:
            data = Saver.decompress_turk(request.forms[key])
            filename = ('turk_' + 
                    time.strftime('%m%d%H%M%S', time.gmtime())
                    + key + '.json')
            filename = os.path.join(self.outdir, filename)
            while os.path.exists(filename):
                # Avoid collision
                filename += 'x'
            with open(filename, 'w') as fout:
                fout.write(data)
            print 'Saved to {}'.format(filename)

    @staticmethod
    def decompress_turk(compressed):
        data = base64.b64decode(compressed)
        data = zlib.decompress(data)
        return data

    def load(self, filename):
        opener = gzip.open if filename.endswith('.gz') else open
        with opener(os.path.join(self.outdir, filename)) as fin:
            return json.load(fin)

    def list_files(self):
        return sorted(os.listdir(self.outdir))

saver = Saver()

@app.hook('after_request')
def enable_cors():
    # This is dangerous but whatever:
    response.headers['Access-Control-Allow-Origin'] = '*'

@app.post('/record')
def record():
    filename = saver.save(request.body.read())
    return 'saved to {}'.format(filename)

@app.post('/mturk/externalSubmit')
def turk():
    saver.save_turk(request)
    return 'saved'

@app.get('/list')
def list_files():
    return {'filenames': saver.list_files()}

@app.get('/view')
def view():
    filename = request.query.filename
    return {
        'filename': filename,
        'episode': saver.load(request.query.filename)
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8032,
            help='Open the connection at this port')
    parser.add_argument('outdir',
            help='Directory to dump the demonstrations')
    parser.add_argument('-g', '--global-access', action='store_true',
            help='Allow global access to the server')
    args = parser.parse_args()

    saver.init_directory(args.outdir)

    # Start the server
    host = 'localhost' if not args.global_access else '0.0.0.0'
    app.run(host=host, port=args.port)
    print '\nGood bye!'
    

if __name__ == '__main__':
    main()

