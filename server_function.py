import os #Import modul os

# Fungsi untuk mengambil konten file dari file yang diminta client
def get_file_content(filename):
    with open(filename, 'rb') as file:
        return file.read() # Membaca seluruh konten file yang telah dibuka

# Fungsi untuk membuat HTTP 404 Not Found response message
def file_not_found():
    content = get_file_content("404page.html") #mengambil konten file dari file yang diminta client
    response_header = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(content)}\r\n\r\n" ## Membuat string yang berisi header HTTP response yang akan dikirimkan ke client
    response = response_header.encode() + content # mengirimkan response header dengan status 404 Not Found
    return response

# fungsi file_serve adalah untuk melayani file yang diminta oleh client
# fungsi ini membuka dan membaca isi file lalu membuat header response yang sesuai dengan panjang dari isi kontent 
# jika file ada akan mengirim header response file tersebut dan jika tidak ada akan mengirim header response 404 Not Found
# lalu me-return header response dan isi konten
def file_serve(filename):
    try:
       content = get_file_content(filename) # mengambil konten file dari file yang diminta client
       response_header = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n" # Membuat string yang berisi header HTTP response yang akan dikirimkan ke client
       response = response_header.encode() + content # mengirimkan response header dengan status 200 OK, serta panjang kontent(content length) yang diambil dari (content)
    except FileNotFoundError:
        response = file_not_found() # mengirimkan response 404 not Found
        print(f"'{filename}' file cant be found!") 
               
    return response

# fungsi get_http_response adalah untuk menangani permintaan atau request dari client
# fungsi ini akan menerima socket dan alamat client lalu menerima request
# memeriksa apakah file request ada atau tidak dan jika file ada akan memanggil fungsi serve_file dan jika tidak ada akan mengirim header response 404 Not Found
def get_http_response(request):
    request_part = request.split()
    method = request_part[0]
    filename = request_part[1][1:]
    if os.path.isfile(filename):  # mengecek apakah file yang diminta terdapat pada direktori
        response = file_serve(filename)
    else:
        response = file_not_found() # mengirimkan response 404 not Found
        print(f"'{filename}' file cant be found!") 
    return response

# fungsi def handle_request untuk menangani koneksi dan menerima request dari client,
# memproses request menggunakan fungsi get_http_response dan mengirimkan response kembali ke client
# Fungsi ini akan mencetak informasi seputar request yang diterima.
def request_handler(client_socket,client_address):
    request = client_socket.recv(4096).decode() # Menerima permintaan dari client

    if request: # Memeriksa permintaan yang diterima
        method, path, protocol = request.split('\n')[0].split() # Memecah permintaan menjadi tiga bagian yaitu method, path, dan protocol
      # Mencetak informasi method, path, dan protocol ke console
        print(f'"{method} {path} {protocol}"\r\n')

        response = get_http_response(request) # Mengambil response HTTP dan mengirimkan tanggapan ke client
        client_socket.sendall(response) # Memastikan seluruh data terkirim
    client_socket.close() # Menutup koneksi ke client
