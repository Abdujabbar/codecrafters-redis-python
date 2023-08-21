# Uncomment this to pass the first stage
import socket
import threading


def execute_process(server_socket):
    conn, address = server_socket.accept()
    
    while conn:
        data = conn.recv(1024).decode()
        partials = list(filter(None, data.split("\r\n")))
        
        if not partials:
            return
        
        _, _, command, *args = partials
        command = command.lower()
        
        if command == 'ping':
            conn.send("$4\r\nPONG\r\n".encode())
        elif command == 'echo':
            partials.append('')
            conn.send('\r\n'.join(partials[3:]).encode())
        else:
            raise Exception('Not Implemented')
    
    
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
