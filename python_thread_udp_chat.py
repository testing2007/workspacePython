import socket
import threading

def recv(udp_socket):
    while True:
        recv_data = udp_socket.recvfrom(1024)
        print("接受的数据=%s" % recv_data)

def send(udp_socket, dest_ip, dest_port):
    while True:
        send_data = input("请输入要发送的内容:")
        udp_socket.sendto(send_data.encode("utf-8"), (dest_ip, dest_port)) #发送数据使用utf-8编码

def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 7000)) #bind参数是一个元组

    dest_ip = input("请输入目标IP") 
    dest_port = int(input("请输入目标port")) #端口要转换int

    t_recv = threading.Thread(target=recv, args=(udp_socket,))
    t_send = threading.Thread(target=send, args=(udp_socket, dest_ip, dest_port))
    t_recv.start()
    t_send.start()


if __name__ == "__main__":
    main()
