
import socket

from Core import Innit
from Core import Instr

port = 1142
host = '0.0.0.0'
max_conn = 2
server = Innit.CreateServer(host,port,max_conn)

precursor = "AFPM\nFUCK FURFAGS\n"
is_avabile = True

while True:
    conn, address = server.accept()
    print(f"[+] We got a conection from '{address}'")
    print(f"[{address}] [+] We are waiting to recive initial data...")
    try:
        initial_data = conn.recv(1024)
        if not initial_data:
            print(f"[{address}] [-] We did not recive any data so we closed the connection...")
            conn.close()
        else:
            Instr.ExecuteRequest(address,precursor,is_avabile,conn,initial_data)
            conn.close()
    
        conn.close()
    except Exception as e:
        print(f"[{address}] [-] ERROR OCCURED '{e}'")
        
