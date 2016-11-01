import socket, select
import commands

CONNECTION_LIST = []
RECV_BUFFER = 4096
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("172.23.101.47", PORT))
server_socket.listen(10)

CONNECTION_LIST.append(server_socket)

flag = True
while flag:
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
    for sock in read_sockets:
        if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

        else:
            data = sock.recv(RECV_BUFFER)
            if data == "start":
                print " start the test"
                cmd = " python perfrunner/utils/ycsb_redis.py &"
                status, output = commands.getstatusoutput(cmd)
                f = open('/root/redis-ycsb/ycsb_log.txt','w')
                sock.send(f.read())
                f.close()

server_socket.close()