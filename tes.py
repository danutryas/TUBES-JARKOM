import socket
import os

def get_file_content(filename):
    with open(filename, 'rb') as file:
        return file.read()
        
def file_not_found(client_socket,filename):
    response_header = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
    client_socket.send(response_header.encode())
    print(f"File {filename} tidak ditemukan pada directory")

def Serv(client_socket, filename):
    try:
       content = get_file_content(filename)
       response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n"
       client_socket.send(response_header.encode())
       client_socket.send(content)
    except FileNotFoundError:
        file_not_found(client_socket,filename)

def get_http_response(request):
    request_part = request.split()
    method = request_part[0]
    filename = request_part[1][1:]
    if os.path.isfile(filename):
        content = get_file_content(filename)
        response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n"
        response = response_header.encode() + content
    else:
        response_header = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
        response = response_header.encode()
        print(f"file {filename} tidak ditemukan di directory")
    return response

def request_handler(client_socket,address):
    request = client_socket.recv(1024).decode()
    if request:
        method, path, protocol = request.split('\n')[0].split()
        print("Permintaan File Berhasil dibuka")
        print("Method: ", method)
        print("Path: ", path)
        print('Protocol: ', protocol)

        response = get_http_response(request)
        client_socket.sendall(response)
    client_socket.close()

def main():
    port = 2112
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))

    server_socket.listen(1)
    print("Server is running...")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Receiving Connection from {address}")
        request_handler(client_socket, address)

if __name__ == "__main__":
    main()