import socket
import struct
import json

# from uploadFile.file_handler import FileHandler
import file_handler as fh
import config as cfg
fh = fh.FileHandler()

def handle_request(new_socket):
    while True:
        try:
            # 首先获取长度
            head_struct = new_socket.recv(4)
            if not head_struct:
                break

            head_len = struct.unpack('i', head_struct)[0]
            head_json = new_socket.recv(head_len).decode('utf-8')
            head_dict = json.loads(head_json)

            # print(head_dict)
            cmd = head_dict['cmd']
            if cmd == cfg.const.UPLOAD_SCREEN_SHOT:
                file_size = head_dict['filesize']
                file_name = head_dict['filename']
                file_path = fh.generateErrorRecvImagePath(file_name)
                # print(file_path)

                recv_size = 0
                recv_data = 0
                with open(file_path, 'wb') as f:
                    while file_size > 0:
                        if(file_size >= cfg.const.TCP_RECEIVE_SIZE):
                            recv_data = new_socket.recv(cfg.const.TCP_RECEIVE_SIZE)
                        else:
                            recv_data = new_socket.recv(file_size)
                        f.write(recv_data)
                        recv_size = len(recv_data)
                        file_size -= recv_size
                    else:
                        # print('recvsize:%s filesize:%s' %
                        #       (recv_size, file_size))
                        # 发送的数据 dict->json->bytes
                        head_dic={'cmd':cfg.const.UPLOAD_SCREEN_SHOT_FINISH, 'serverpath':file_path}
                        print(head_dic)
                        head_json = json.dumps(head_dic)
                        head_json_bytes = bytes(head_json, encoding='utf-8')

                        # 先发送数据长度, 再发送数据
                        head_struct = struct.pack('i', len(head_json_bytes))
                        new_socket.send(head_struct)
                        new_socket.send(head_json_bytes)
                        
        except Exception:
            break


def main():
    print("main")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((cfg.const.SERVER_IP, cfg.const.SERVER_PORT))
    server_socket.listen(1024)

    while(True):
        # 阻塞等待
        new_connect_socket, client_addr = server_socket.accept()
        
        # 新的连接处理
        handle_request(new_connect_socket)

    # 关闭套接字
    new_connect_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()