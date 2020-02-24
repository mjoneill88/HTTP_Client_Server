Http-socket-program
Implementation of HTTP client and server that run a simplified version of HTTP/1.1

HTTP Server file (server.py):

python server <port>
Example: python server.py 5000
HTTP Client file (client.py):

python client.py <hostname> <port> <command(GET/POST)> <filename>
Example:
GET Request: python client.py 127.0.0.1 5000 GET testfile
PUT Request: python client.py 127.0.0.1 5000 PUT testfile
Ref: https://docs.python.org/3/library/socket.html
