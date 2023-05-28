#Melakukan import modul
import socket #Import modul socket
from server_function import * # Import functions dari file server_function.py

# fungsi utama dalam membuat socket server
# mem-bind ke port yang sudah ditentukan yaitu 2112
# melakukan penanganan terhadap setiap permintaan koneksi yang masuk dengan memanggil fungsi request_handler
def main():
    port = 2112 # Inisialisasi port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Membuat socket baru untuk server
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1) # Membuat socket agar socket dapat digunakan lagi
    server_socket.bind(('', port)) # Socket di-bind ke port 2112

    server_socket.listen(1) # Menjalankan server
    print("\nServer is running...\n")

    while True: # Melakukan loop agar server terus berjalan
        client_socket, client_address = server_socket.accept() # Server menerima koneksi dari client
        print(f"Receiving Connection from {client_address}")
        request_handler(client_socket, client_address) # untuk handle request koneksi baru yang akan membaca request dari clien dan mengirimkan response yang sesuai dengan request tersebut

# Menjalankan Fungsi main ketika di-run
if __name__ == "__main__":
    main()