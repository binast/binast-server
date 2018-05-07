#!/usr/bin/env python
import os
import ssl
import sys
import BaseHTTPServer

HOST = 'localhost'
PORT = 8443

CONTENT_TYPES = {
    '.css': 'text/css; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.php': 'application/x-httpd-php',
    '.htm': 'text/html',
    '.html': 'text/html'
}

www_path = os.getcwd()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        file_path = s.path.lstrip('/')
        if '?' in file_path:
            file_path = file_path[:file_path.rindex('?')]
            print "Fixed path", file_path
        path = os.path.join(www_path, file_path)

        headers = s.headers
        accept = headers['Accept'].lower().split(',')
        accepts_binast = 'application/javascript-binast' in accept

        print 'Received header:\n' + str(headers) + '\n'

        if not os.path.exists(path):
            print 'Path does not exist:', path
            s.send_response(404)
            s.send_header('Content-type', 'text/html; charset=utf-8')
            s.end_headers()
            s.wfile.write('404 File not found')
            return

        s.send_response(200)

        file_ext = os.path.splitext(path)[1].lower()

        if file_ext == '.js':
            binast_path = path.rstrip('.js') + '.binjs'
            if accepts_binast and os.path.exists(binast_path):
                path = binast_path
                s.send_header('Content-type', 'application/javascript-binast')
            else:
                s.send_header('Content-type', 'application/javascript')
        elif file_ext in CONTENT_TYPES:
            s.send_header('Content-type', CONTENT_TYPES[file_ext])
        else:
            print 'Error: unrecognized content type:', file_ext, "from", path
            s.send_header('Content-type', 'text/plain;charset=utf8')

        s.end_headers()
        s.wfile.write(open(path, 'r').read())

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        www_path = sys.argv[1]

    server = BaseHTTPServer.HTTPServer((HOST, PORT), MyHandler)
    server.socket = ssl.wrap_socket (server.socket, certfile='./server.pem', server_side=True)

    print 'Ready, listening for HTTPS on', HOST, PORT
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

