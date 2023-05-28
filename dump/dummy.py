import socket
import os

# Fungsi untuk mengambil konten file dari file system
def get_file_content(filename):
    with open(filename, 'rb') as file:
        return file.read()

# Fungsi untuk membuat HTTP response message
def create_response(filename, content_type, content):
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: {}\r\n".format(content_type)
    response += "Content-Length: {}\r\n".format(len(content))
    response += "\r\n"
    response += content.decode('utf-8')
    return response

# Fungsi untuk membuat HTTP 404 Not Found response message
def create_404_response():
    filepath = "404page.html"
    content_type = 'text/html' #if filepath.endswith('.html') else 'text/css'
    content = get_file_content(filepath)
    response = "HTTP/1.1 404 Not Found\r\n"
    response += "Content-Type: {}\r\n".format(content_type)
    response += "Content-Length: {}\r\n".format(len(content))
    response += "\r\n"
    #response += content.decode('utf-8')
    response = create_response(filepath, content_type, content)
    return response

# Inisialisasi host dan port
port = 2223

# Buat TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket ke alamat dan port tertentu
server_socket.bind(('', port))

# Listen koneksi masuk
server_socket.listen(1)
print('Server sudah siap untuk digunakan...')

while True:
    # Terima koneksi dari client
    client_socket, client_address = server_socket.accept()
    print('Menerima koneksi dari: ', client_address)

    # Terima data dari client
    request_data = client_socket.recv(1024).decode('utf-8')

    # Parse HTTP request
    request_lines = request_data.split('\r\n')
    request_method, request_path, _ = request_lines[0].split()

    if request_method == 'GET':
        # Cari dan ambil file yang diminta oleh client
        filepath = request_path[1:]  # Hapus leading slash ("/")
        if os.path.isfile(filepath):
            if filepath.endswith('.pdf'):
                content_type = 'application/pdf'
            else:
                content_type = 'text/html' if filepath.endswith('.html') else 'text/css'
            content = get_file_content(filepath)
            response = create_response(filepath, content_type, content)
        else:
            response = create_404_response()
    else:
        # Jika method selain GET, kirim response dengan pesan "404 Not Found"
        response = create_404_response()

    # Kirim response ke client
    client_socket.sendall(response.encode('utf-8'))

    # Tutup koneksi
    client_socket.close()