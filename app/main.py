# Uncomment this to pass the first stage
import socket
import threading
import time


class StorageSet(dict):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = dict.__new__(cls, *args, **kwargs)
        
        return cls._instance


def execute_process(server_socket, storage):
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
        elif command == 'set':
            partials = partials[3:]
            expire = 10 ** 30
            if len(partials) > 4:
                expire = int(partials[-1]) / 1000
            key = partials[1]
            value = partials[3]
            storage[key] = (value, expire, time.time())
            conn.send("$2\r\nOK\r\n".encode())
        elif command == 'get':
            partials = partials[3:]
            key = partials[-1]
            if key in storage:
                value, expire, prev_time = storage.get(key)
                curr_time = time.time()

                if curr_time - prev_time > expire:
                    conn.send(f"$-1\r\n".encode())
                
                conn.send(f'${len(value)}\r\n{value}\r\n'.encode())
            else:
                conn.send(f"$-1\r\n".encode())
        else:
            raise Exception('Not Implemented')
    
    
def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    storage = StorageSet()
    threads = []

    for _ in range(20):
        x = threading.Thread(target=execute_process, args=(server_socket, storage,))
        threads.append(x)
        x.start()

    for _, thread in enumerate(threads):
        thread.join()


if __name__ == "__main__":
    main()

