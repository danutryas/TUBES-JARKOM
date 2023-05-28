#Melakukan import modul
import socket #Import modul socket
import os #Import modul os

# Fungsi untuk mengambil konten file dari file yang diminta client
def get_file_content(filename):
    with open(filename, 'rb') as file:
        return file.read()
    
def file_not_found():
   # response_header = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
   # client_socket.send(response_header.encode())
   # print(f"'{filename}' file cant be found!")
    content = get_file_content("404page.html")
    response_header = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(content)}\r\n\r\n"
    response = response_header.encode() + content
    return response

#def Serve(client_socket, filename):
    try:
       content = get_file_content(filename)
       response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n"
       client_socket.send(response_header.encode())
       client_socket.send(content)
    except FileNotFoundError:
        file_not_found(client_socket,filename)

#
def get_http_response(request):
    request_part = request.split()
    method = request_part[0]
    filename = request_part[1][1:]
    if os.path.isfile(filename):
        content = get_file_content(filename)
        response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n"
        response = response_header.encode() + content
    else:
        response = file_not_found()
        print(f"'{filename}' file cant be found!")
    return response

def request_handler(client_socket,client_address):
    request = client_socket.recv(4096).decode()

    if request:
        method, path, protocol = request.split('\n')[0].split()
        print(f'"{method} {path} {protocol}"\r\n')

        response = get_http_response(request)
        client_socket.sendall(response)
    client_socket.close()

def main():
    port = 2112
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind(('', port))

    server_socket.listen(1)
    print("\nServer is running...\n")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Receiving Connection from {client_address}")
        request_handler(client_socket, client_address) 

if __name__ == "__main__":
    main()