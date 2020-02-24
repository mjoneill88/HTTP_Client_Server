#!/usr/bin/env python3

import socket, time, os, threading


class MyServer(object):
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.public_dir = 'public'
        self.host = host
        self.port = port

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        while True:
            (client, address) = self.s.accept()
            client.settimeout(50)
            print('Connected by client ', address)
            threading.Thread(target=self._handle_client, args=(client, address)).start()

    def _handle_PUT(self, data, client, file_requested):
        # while True:
            # data = client.recv(1024)
        #print(data)
        try:
            # f = open(file_requested, 'w')
            # f.write(data)
            #f.close()
            response_header = self._generate_headers(200)
            response = response_header.encode()
        except Exception as e:
            print("__PUT func", e)
            response_header = self._generate_headers(404)
            response = response_header.encode()
        client.send(response)


    def _handle_GET(self, data, client, file_requested):
        try:
            #print("file--", file)
            f = open(file_requested, 'rb')
            response_data = f.read()
            f.close()
            response_header = self._generate_headers(200)
            response = response_header.encode()
            response += response_data
        except Exception as e:
            print("_handle_GET error: File not found !", e)
            response_header = self._generate_headers(404)
            response = response_header.encode()
        print("Response header: ", response)
        client.send(response)
        client.close()


    def _handle_client(self, client, address):
        self.current_req_state = None
        self.file_requested = None
        try:
            # self.s.bind((self.host, self.port))
            # self.s.listen()
            # self.conn, self.addr = self.s.accept()
            # print('Connected by client ', self.addr)
            while True:
                #print("______ self.current_req_state____", self.current_req_state)
                data = client.recv(1024)
                print("+++++ Data recv ++++++", data)
                if not data:
                    # if self.current_req_state =="PUT":
                    #     response_header = self._generate_headers(201)
                    #     response = response_header.encode()
                    #     client.send(response)
                    self.current_req_state = None
                    print("Connection closed by client ", address)
                    client.close()
                    break
                if self.current_req_state =="PUT":
                    print("PUT DATA ->>>>>>", data.decode())
                    f = open(self.file_requested, 'wb')
                    f.write(data)
                    f.close()
                    response_header = self._generate_headers(201)
                    response = response_header.encode()
                    client.send(response)
                    client.close()
                try:
                    parsed_req = data.decode().split()
                    # print(parsed_req)
                    self.file_requested =  (parsed_req[1].split('?')[0]).split('/')[1]
                except:
                    pass
                #file_requested = os.path.join(self.public_dir, file_requested.split('/')[1])
                #file_requested = file_requested.split('/')[1]
                print("file_requested: ", self.file_requested)
                if parsed_req[0] == "GET":
                    self.current_req_state = "GET"
                    print("GET Request received from client for %s" %(self.file_requested))
                    self._handle_GET(data, client, self.file_requested)
                    break
                elif(parsed_req[0] == "PUT"):
                    self.current_req_state = "PUT"
                    print("PUT Request received from client for %s" %(parsed_req[1]))
                    self._handle_PUT(data, client, self.file_requested)
                else:
                    pass
                    # print("Wrong Request")
                    # response_header = self._generate_headers(404)
                    # client.send(response_header)
                    # client.close()
            #client.close()
        except Exception as e:
            print("_handle_client ERROR!!", e)



    def _generate_headers(self, response_code):
        """ Generate HTTP response headers """
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'
        elif response_code == 201:
            header += 'HTTP/1.1 200 OK File Created\n'
        else:
            header += 'HTTP/1.1 400 Bad Request\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Connection: close\n\n'
        return header

    # def _send_data(self, data_response):
    #     self.conn.send(data_response)
    #     return
    #     #self.conn.close()


if __name__ == "__main__":
    import sys
    HOST = '127.0.0.1' #sys.argv[1] #
    PORT = int(sys.argv[1]) #4000
    ms = MyServer(HOST, PORT)
    ms.start()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by client ', addr)
#         while True:
#             data = conn.recv(1024)
#             print(data)
#             if not data:
#                 break
#             conn.sendall(data)
