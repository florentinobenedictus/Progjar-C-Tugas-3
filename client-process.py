import sys
import socket
import logging
import threading
from multiprocessing import Process

def kirim_data(nama="kosong"):
    logging.warning(f"[PROCESS KE- {nama}]")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning(f"[PROCESS KE- {nama}] membuka socket")

    server_address = ('172.22.0.2', 45000)
    logging.warning(f"[PROCESS KE- {nama}] opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME 1310'
        logging.warning(f"[PROCESS KE- {nama}] [CLIENT] sending {message}")
        sock.sendall(message.encode())
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            logging.warning(f"[PROCESS KE- {nama}] [DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning(f"[PROCESS KE- {nama}] closing")
        sock.close()
    return


if __name__=='__main__':
    processes = []
    num_processes = 100
    for i in range(num_processes):
        p = Process(target=kirim_data, args=(i,))
        processes.append(p)

    for pro in processes:
        pro.start()