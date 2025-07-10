
import socket

def CreateServer(host:str,port:int,max_conn:int) -> socket.socket:
    print(f"[+] Creating AFPM server on host '{host}' and port '{port}'...")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((host,port))
    print(f"[+] Listening on host '{host}' with maximum client connection of {max_conn}...")
    sock.listen(max_conn)

    return sock