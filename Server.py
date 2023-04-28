import os
import socket

def GET (connection, fPath, clength):
    if not os.path.exists(fPath):
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        connection.sendall(response.encode())
        return
    
    content_type = 'text/plain'
    x = fPath.index('.')
    temp_content = fPath[x:]
    if temp_content == '.html':
        content_type = 'text/html'
    if temp_content == '.png':
        content_type = 'image/png'
    
    with open(fPath) as file:
        file_Content = file.read()
        
    response = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nfile_Content: {}\r\n\r\n'.format(content_type, clength)
    connection.sendall(response.encode() + file_Content.encode())

def HEAD(connection, fPath, ctype, clength):
    if not os.path.exists(fPath):
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        connection.sendall(response.encode())
        return
    print(ctype)
    with open(fPath) as file:
        file_Content = file.read()
    
    response = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nfile_Content: {}\r\n\r\n'.format(ctype, clength)
    connection.sendall(response.encode())

def POST(connection, fPath, body, clength):
    if not fPath.endswith('.txt'):
        response = 'HTTP/1.1 400 BAD REQUEST\r\n\r\n'
        connection.sendall(response.encode())
        return
    if fPath.endswith('.txt'):
        have = os.path.exists(fPath)
        response_message = '200 OK'
        with open(fPath, 'ab') as file:
            file.write(body.encode('utf-8'))
        if not have:
            response_message = '201 Created'
        response = 'HTTP/1.1 {}\r\nContent-Type: text/plain\r\nbody: {}\r\n\r\n'.format(response_message, clength)
    else:
        response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
    
    connection.sendall(response.encode())
    

def PUT(connection, fPath, body, ctype, clength):
    removed = False
    if os.path.exists(fPath):
        os.remove(fPath)
        removed = True
    with open(fPath, 'ab') as file:
        file.write(body.encode('utf-8'))
    if not removed:
        response_message = '201 Created'
    else: 
        response_message = '200 OK'
    response = 'HTTP/1.1 {}\r\nContent-Type: {}\r\nbody: {}\r\n\r\n'.format(response_message, ctype, clength)
    connection.sendall(response.encode())

def DELETE(connection, fPath, ctype, clength):
    removed = False
    if os.path.exists(fPath):
        os.remove(fPath)
        removed = True
    if removed:
        response_message = '200 OK'
    else:
        response_message = '404 NOT FOUND'
    response = 'HTTP/1.1 {}\r\nContent-type: {} \r\nbody: {}\r\n\r\n'.format(response_message, ctype, clength)
    connection.sendall(response.encode())

def server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8888))

    serversocket.listen()


    while True:
        clientsocket, address = serversocket.accept()

        receive = clientsocket.recv(1024).decode()
        rt, rp, rv = receive.split('\r\n')[0].split()
        rp = rp[1:]
        rl = receive.split('\r\n')
        ctype = rl[1][14:]
        body = rl[-1]
        clength = int(rl[-3][16:])
        if rt == 'GET':
            GET(clientsocket, rp, clength)

        if rt == 'POST':
            POST(clientsocket, rp, body, clength)
        
        if rt == 'PUT':
            PUT(clientsocket, rp, body, ctype, clength)

        if rt == 'DELETE':
            DELETE(clientsocket, rp, ctype, clength)

        if rt == 'HEAD':
            HEAD(clientsocket, rp, ctype, clength)
        
        clientsocket.close()

if __name__ == '__main__':
    server()