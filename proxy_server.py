#source cmput 404 Lab2
import socket, sys
from multiprocessing import Process


HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# get ip address
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():

    host = "www.google.com"
    port = 80

    #create socket, get remote ip, and connect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        #allow reused addresses, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            p = Process(target=handle_proxy, args=(conn,  host, port))
            p.daemon = True
            p.start()
            print("Started process", p)

           
            

def handle_proxy(conn, host, port):
   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        print("Connecting to Google")
        remote_ip = get_remote_ip(host)

        #connect proxy_end
        proxy_end.connect((remote_ip, port))

        #send data
        send_full_data = conn.recv(BUFFER_SIZE)
        print(f"Sending received data {send_full_data} to google")
        proxy_end.sendall(send_full_data)

        #shutdown
        proxy_end.shutdown(socket.SHUT_WR)

        data = proxy_end.recv(BUFFER_SIZE)
        print(f"Sending received data {data} to client")
        #send data back
        conn.send(data)
        #close
    conn.close()
   
    
    

if __name__ == "__main__":
    main()