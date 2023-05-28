import os #Import modul os

def get_file_content(filename):
    with open(filename, 'rb') as file:
        return file.read()
    
def file_not_found():
    content = get_file_content("404page.html")
    response_header = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(content)}\r\n\r\n"
    response = response_header.encode() + content
    return response

def file_serve(filename):
    try:
       content = get_file_content(filename)
       response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n"
       response = response_header.encode() + content
    except FileNotFoundError:
        response = file_not_found()
        print(f"'{filename}' file cant be found!") 
               
    return response

def get_http_response(request):
    request_part = request.split()
    method = request_part[0]
    filename = request_part[1][1:]
    response = file_serve(filename)
    return response

def request_handler(client_socket,client_address):
    request = client_socket.recv(4096).decode()

    if request:
        method, path, protocol = request.split('\n')[0].split()
        print(f'"{method} {path} {protocol}"\r\n')

        response = get_http_response(request)
        client_socket.sendall(response)
    client_socket.close()