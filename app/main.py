# Uncomment this to pass the first stage
from codecrafters_redis_python.redis_server import RedisServer, StorageSet


    
def main():
    print("Logs from your program will appear here!")
    RedisServer("localhost", 6379, StorageSet()).run()
    

if __name__ == "__main__":
    main()

