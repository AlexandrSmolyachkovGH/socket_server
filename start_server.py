import socket
import datetime


def start_socket_server():
    try:
        # implementation of bind method makes our socket a server
        # socket.AF_INET -> soket for processing with IPv4 (Internet Protocol version 4)
        # socket.SOCK_STREAM -> stream socket with using consistent two-way connection
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 2000))

        # the instructions below do the same thing as written above
        # server_socket = socket.create_server(('127.0.0.1', '2000'))
        # set the number of clients that can be queued
        server_socket.listen(5)
        while True:
            print('Start the server')
            # method .accept() set the connection between server and client and lock program processing up to getting
            # connection
            client_socket, address = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            # print(f'Data: {data}')
            content = load_page_from_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server_socket.close()
        print('Stop the server')


def load_page_from_request(request):
    HDRS = 'HTTP/1.1 200 OK\r\n\Content-Type: text/html; charset=utf-8\r\n\r\n'
    path = request.split(' ')[1]
    if path != '/time.html':
        path = '/base.html'
    else:
        cdt = get_current_datetime()
        cdt = cdt.strftime("Current time: %H:%M:%S \n Current date: %d-%M-%Y ").encode('utf-8')
    response = ''
    with open('views' + path, 'rb') as file:
        response = file.read()
        if path == '/time.html':
            response = response.replace(b'cdt_index', cdt)
    return HDRS.encode('utf-8') + response

def get_current_datetime():
    return datetime.datetime.now()

if __name__ == "__main__":
    start_socket_server()
