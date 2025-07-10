
from Core import FileStem
import os

def ExecuteRequest(address:str,precursor:str,is_avabile:bool,conn,initial_data:str):
    try:
        print(f"[{address}] [+] We recived initial data!")
        print(f"[{address}] [+] We are verifying initial data...")
        initial_data = initial_data.decode()
        if initial_data.startswith(precursor):
            print(f"[{address}] [+] Data is valid!")
            print(f"[{address}] [+] Must find the protocol request!")
            initial_data = initial_data.removeprefix(precursor)
            match initial_data:
                case 'PING':
                    print(f"[{address}] [+] Request was PING!")
                    if is_avabile:
                        conn.send((precursor + "ONLINE").encode())
                        print(f"[{address}] [+] Responded with ONLINE!")
                    else:
                        conn.send((precursor + "UNREACHABLE").encode())
                        print(f"[{address}] [+] Responded with UNREACHABLE!")
                case _:
                    if initial_data.startswith("QUERY"):
                        print(f"[{address}] [+] Request is a QUERY!")
                        data = initial_data.split("\n")
                        query_for = data[1]
                        exists,file_locs = FileStem.GetPackData(query_for)

                        if not exists:
                            conn.send((precursor + "NOT FOUND").encode())
                        else:
                            conn.send((precursor + "FOUND\n" + "\n".join(file_locs)).encode())
                    elif initial_data.startswith("DOWNLOAD"):
                        print(f"[{address}] [+] Request is a DOWNLOAD!")
                        data = initial_data.split("\n")
                        query_for = data[1]
                        exists,file_locs = FileStem.GetPackData(query_for)

                        if not exists:
                            conn.send((precursor + "NOT FOUND").encode())
                        else:
                            headers = []
                            for file in file_locs:
                                headers.append(file.lstrip("packs/").encode() + b"\n" + str(os.path.getsize(file)).encode())
                            conn.sendall(b'\n'.join(headers) + b"\x00")
                            conn.recv(1024)
                            headers = []
                            for file in file_locs:
                                headers.append(open(file,"rb").read())
                            conn.sendall(b''.join(headers))
                    else:
                        print(f"[{address}] [-] Request was not specified!")
                        conn.send((precursor + "INVALID REQUEST").encode())
        else:
            print(f"[{address}] [-] Data is invalid!")
            conn.send((precursor + "INVALID REQUEST").encode())
    except Exception as e:
         print(f"[{address}] [-] Error occured '{e}'")
         conn.send((precursor + "INTERNAL ERROR").encode())
    conn.close()