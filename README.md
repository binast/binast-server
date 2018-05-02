# binast-server
Running server:
```
./serveBinAST.py [PORT=8443]
```

To test in browser: load https://localhost:8443/hello.html, accept self-signed localhost cert, confirm output is 'Script run status: BINAST'

To test in commandline:
```
wget --header="Accept: application/javascript-binast, */*" -S -O - --no-check-certificate https://localhost:8443/hello.js
```

Expected output:
```
--2018-05-02 12:48:05--  https://localhost:8443/hello.js
Resolving localhost... ::1, 127.0.0.1
Connecting to localhost|::1|:8443... failed: Connection refused.
Connecting to localhost|127.0.0.1|:8443... connected.
WARNING: cannot verify localhost's certificate, issued by 'CN=localhost,O=Personal,C=US':
  Self-signed certificate encountered.
HTTP request sent, awaiting response...
  HTTP/1.0 200 OK
  Server: BaseHTTP/0.3 Python/2.7.10
  Date: Wed, 02 May 2018 19:48:05 GMT
  Content-type: application/javascript-binast
Length: unspecified [application/javascript-binast]
Saving to: 'STDOUT'

document.getElementById('status').innerText = 'BINAST';

2018-05-02 12:48:05 (2.81 MB/s) - written to stdout [56]
```
