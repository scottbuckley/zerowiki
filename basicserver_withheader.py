#! /usr/bin/env python

import cgi, os, SocketServer, sys, time, urllib, re
from SimpleHTTPServer import SimpleHTTPRequestHandler
from StringIO import StringIO
import BaseHTTPServer

import pickle

class DirectoryHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        if self.path.startswith("/__zwheader"):
            self.generateHeader()
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def generateHeader(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()    

        scanDir()
        refs = getRefs(self.path.split('?')[-1])

        if len(refs)>0:
            reflinks = ['['+a+'](?'+a+')' for a in refs]

            w = self.wfile
            w.write('<div class="zwheader" style="position: absolute; left: 2em; top: 2em;">')
            w.write('Referenced by: ')
            w.write(', '.join(reflinks))
            w.write('</div>')


dump = None
def getDump():
    global dump

    if (dump is None):
        try:
            with open('.zwdump', 'rb') as dumpfile:
                dump = pickle.load(dumpfile)
        except IOError as e:
            print(".zwdump was not found. Starting from scratch over here.")
            dump = {}

    return dump

def saveDump():
    d = getDump()
    with open('.zwdump', 'wb') as dumpfile:
        pickle.dump(d, dumpfile)

linkpatt = re.compile("\]\(([^\)]+?\.md)(?:\#[^\)]*?)?\)")
def processFile(fname):
    print("scanning updated file '"+ fname + "'.")
    d = getDump()
    with open(fname, "r") as myfile:
        data=myfile.read()
    links = re.findall(linkpatt, data)

    d[fname]['links'] = links

def scanFile(fname):
    d = getDump()
    if fname not in d:
        d[fname] = {}
        d[fname]['lastchecked'] = 0

    date_checked  = d[fname]['lastchecked']
    date_modified = int(os.path.getmtime(fname))

    if date_modified > (date_checked):
        processFile(fname)
        d[fname]['lastchecked'] = int(time.time())
        return True
    return False

def getRefs(fname):
    d = getDump()
    out = []
    for otherfile in d:
        if 'links' in d[otherfile]:
            if fname in d[otherfile]['links']:
                out.append(otherfile)
    return out

def scanDir():
    dr = os.listdir(os.getcwd())
    dr = [f for f in dr if os.path.isfile(f) and f.endswith('.md')]
    s = False

    for f in dr:
        if scanFile(f):
            s = True

    if s:
        saveDump()



if __name__=="__main__":
   BaseHTTPServer.test(DirectoryHandler, BaseHTTPServer.HTTPServer)


