import socket

# Inisialisasi host dan port
host = "localhost"
port = 2223

# Buat TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Terhubung ke server
client_socket.connect((host, port))
print('Anda telah terhubung ke server: {}:{}'.format(host, port))

while True:
    # Minta input dari pengguna
    path = input('Masukkan nama file yang ingin anda akses: ')

    # Kirim permintaan HTTP ke server
    request = "GET {}\r\n".format(path)
    client_socket.sendall(request.encode('utf-8'))

    # Terima dan tampilkan response dari server
    response = client_socket.recv(1024).decode('utf-8')
    print('Response dari server:')
    print(response)

    # Tanyakan kepada pengguna apakah ingin melanjutkan atau tidak
    choice = input('Lanjutkan? (y/n): ')
    if choice.lower() != 'y':
        break

# Tutup koneksi
client_socket.close()
