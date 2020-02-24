#!/usr/bin/env python3

"""
Client
"""
import socket, requests, sys


def create_request(request_type, file_name, host):
    return """%s /%s HTTP/1.1\r\nHost:%s\r\n\r\n""" %(request_type, file_name, host)


def do_get(s, file_name, host):
    s.sendall(create_request("GET", file_name, host).encode())

def do_PUT(s, file_name, host):
    req_head = create_request("PUT", file_name, host).encode()
    s.sendall(req_head)



if __name__ == "__main__":

    ###########################
    host = sys.argv[1]    # Server addr
    port = int(sys.argv[2])           # Server port
    request_type = sys.argv[3]
    file_name = sys.argv[4]
    print(host, port, request_type, file_name)
    #print(""" server host %s \nserver port %s\n """ )
    ###############################
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        ###########################
        if request_type =="GET":
            do_get(s, file_name, host)
            data = s.recv(1024)
            print("Server Response: ", data)

        elif request_type =="PUT":
            #while True:
            do_PUT(s, file_name, host)
            while True:
                data = s.recv(1024)
                print("PUT Response data ", data)
                if not data:
                    print("No data!")
                    break
                with open(file_name, 'rb') as f:
                    #s.send(f)
                    s.sendfile(f)
                break
            data = s.recv(1024)
            print(data)

        else:
            print("INVALID Request Type")
        # print(create_request(request_type, file_name, host))
        #s.sendall(create_request(request_type, file_name, host).encode())
        # data = s.recv(1024)
        # print('Received', repr(data))
