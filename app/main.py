# Uncomment this to pass the first stage
import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn, address = server_socket.accept()

    while conn:
        data = str(conn.recv(1024))

        if data == '+PING\n\r':
            conn.send('+PONG\n\r'.encode())
    
if __name__ == "__main__":
    main()
