#Melakukan import modul
import socket #Import modul socket
from server_function import *

# Fungsi untuk mengambil konten file dari file yang diminta client


def main():
    port = 2112
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1) #Agar socket dapat digunakan lagi
    server_socket.bind(('', port))

    server_socket.listen(1)
    print("\nServer is running...\n")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Receiving Connection from {client_address}")
        request_handler(client_socket, client_address) 

if __name__ == "__main__":
    main()