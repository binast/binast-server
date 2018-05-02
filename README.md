# binast-server
Running server:
```
./serveBinAST.py [PORT=8443]
```

To test in browser: load https://localhost:8443/hello.html, accept localhost cert, confirm output is 'Script run status: OK'

To test in commandline:
```
wget --header="Accept: application/javascript-binast, */*" -S -O - --no-check-certificate https://localhost:8000/hello.js
```

Expected output:
```
--2018-05-02 12:31:59--  https://localhost:8000/hello.js
Resolving localhost... ::1, 127.0.0.1
Connecting to localhost|::1|:8000... failed: Connection refused.
Connecting to localhost|127.0.0.1|:8000... connected.
WARNING: cannot verify localhost's certificate, issued by 'CN=localhost,O=Personal,C=US':
  Self-signed certificate encountered.
HTTP request sent, awaiting response...
  HTTP/1.0 200 OK
  Server: BaseHTTP/0.3 Python/2.7.10
  Date: Wed, 02 May 2018 19:31:59 GMT
  Content-type: application/javascript-binast
Length: unspecified [application/javascript-binast]
Saving to: 'STDOUT'

-                                                        [<=>                                                                                                                 ]       0  --.-KB/s               document.getElementById('status').innerText = 'OK';
-                                                        [ <=>                                                                                                                ]      52  --.-KB/s    in 0.001s

2018-05-02 12:31:59 (42.7 KB/s) - written to stdout [52]
```
