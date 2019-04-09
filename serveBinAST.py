#!/usr/bin/env python
import os
import ssl
import sys
import StringIO
import gzip
import BaseHTTPServer

HOST = 'localhost'
PORT = 8443

SERVE_GZIP = True

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
    def do_GET(self):
        file_path = self.path.lstrip('/')
        if '?' in file_path:
            file_path = file_path[:file_path.rindex('?')]
            print "Fixed path", file_path
        path = os.path.join(www_path, file_path)

        headers = self.headers
        accept = headers['Accept'].lower().split(',')
        accepts_binast = 'application/javascript-binast' in accept

        if 'Accept-Encoding' in headers:
            accept_encoding = headers['Accept-Encoding'].lower().split(',')
            accepts_gzip = 'gzip' in accept_encoding
        else:
            accepts_gzip = False

        print 'Received header:\n' + str(headers) + '\n'

        if not os.path.exists(path):
            print 'Path does not exist:', path
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('404 File not found')
            return

        self.send_response(200)


        if accepts_gzip and SERVE_GZIP:
            self.send_header('Content-Encoding', 'gzip')

        file_ext = os.path.splitext(path)[1].lower()

        if file_ext == '.js':
            binast_path = path.rstrip('.js') + '.binjs'
            if accepts_binast and os.path.exists(binast_path):
                path = binast_path
                self.send_header('Content-type', 'application/javascript-binast')
            else:
                self.send_header('Content-type', 'application/javascript')

        elif file_ext in CONTENT_TYPES:
            self.send_header('Content-type', CONTENT_TYPES[file_ext])
        else:
            print 'Error: unrecognized content type:', file_ext, "from", path
            self.send_header('Content-type', 'text/plain;charset=utf8')

        self.end_headers()
        file_contents = open(path, 'rb').read()
        if accepts_gzip and SERVE_GZIP:
            file_contents = self.gzip_encode(file_contents)

        self.wfile.write(file_contents)

    def gzip_encode(self, content):
        out = StringIO.StringIO()
        gf = gzip.GzipFile(fileobj=out, mode='wb', compresslevel=5)
        gf.write(content)
        gf.close()
        return out.getvalue()

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

