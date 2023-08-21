# Uncomment this to pass the first stage
import socket
import threading
import concurrent.futures


def execute_process(server_socket):
    conn, address = server_socket.accept()
    print(f"{conn=}, {address=}")
    data = conn.recv(1024).decode()
            
    if not data:
        return
    
    if "ping" in data.lower():
        conn.send("$4\r\nPONG\r\n".encode())
    
    
def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    threads = []

    for _ in range(20):
        x = threading.Thread(target=execute_process, args=(server_socket,))
        threads.append(x)
        x.start()

    for _, thread in enumerate(threads):
        thread.join()


if __name__ == "__main__":
    main()
