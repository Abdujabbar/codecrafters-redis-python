# Uncomment this to pass the first stage
import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        conn, address = server_socket.accept()

        while conn:
            data = conn.recv(1024).decode()
            
            if not data:
                break
            
            if "ping" in data.lower():
                conn.send("$4\r\nPONG\r\n".encode())
    
if __name__ == "__main__":
    main()
