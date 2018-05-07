#!/usr/bin/env python
import os
import ssl
import BaseHTTPServer

HOST = 'localhost'
PORT = 8443

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        path = s.path.lstrip('/')
        path = os.path.join(os.getcwd(), path)

        headers = s.headers
        accept = headers['Accept'].lower().split(',')
        accepts_binast = 'application/javascript-binast' in accept

        print "Received header:\n" + str(headers) + "\n"

        if not os.path.exists(path):
            print "Path does not exist: " + path
            s.send_response(404)
            s.end_headers()
            s.wfile.write('404 File not found')
            return

        s.send_response(200)

        if path.endswith('.js'):
            binast_path = path + '.binjs'
            if accepts_binast and os.path.exists(binast_path):
                path = binast_path
                s.send_header('Content-type', 'application/javascript-binast')
            else:
                s.send_header('Content-type', 'application/javascript')
        else:
            s.send_header("Content-type", "text/html")

        s.end_headers()
        s.wfile.write(open(path, 'r').read())

if __name__ == '__main__':
    server = BaseHTTPServer.HTTPServer((HOST, PORT), MyHandler)
    server.socket = ssl.wrap_socket (server.socket, certfile='./server.pem', server_side=True)

    print "Ready, listening for HTTPS on", HOST, PORT
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

