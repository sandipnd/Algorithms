import select
import socket
import os
from  multiprocessing import Process
import json
BUFSIZE = 4096


class YcsbClient(object):

    def __init__(self, hosts):
        self.hosts = hosts
        self.conn_list = []

    def run_ycsb_server(self):
        """
        copy server file
        run it in background
        """
        pass

    def run_ycsb(self, host):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, 5000))
        self.conn_list.append(conn)
        while True:
            cmd = "start"
            conn.send(cmd)
            select.select([],[conn],[])
            data = conn.recv(BUFSIZE)
            print data

    def run(self):
        self.run_ycsb_server()
        processes = [Process(target=self.run, args=(x,)) for x in range(self.hosts)]
        for p in processes:
            p.start()

        for p in processes:
            p.join()
