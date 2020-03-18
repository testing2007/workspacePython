import socket
import struct
import time
import os
import json

def getCurrentDir():
    return os.getcwd();

def getErrorImageDir():
    error_image_dir = os.path.join(os.getcwd(), "recv_image")
    if not os.path.exists(error_image_dir):
        os.makedirs(error_image_dir)
    return error_image_dir;

def generateErrorImagePath( file_name):
    # random_name = 'test_{}_{}'.format(time.strftime(
    #     '%Y_%m_%d_%H_%M_%S'), random.randint(1, 999))
    # report_name = f'{random_name}.html'
    path_file = os.path.join(getErrorImageDir(), file_name)
    return path_file
    
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

            print(head_dict)
            cmd = head_dict['cmd']
            if cmd == 'UPLOAD_SCREEN_SHOT':
                file_size = head_dict['filesize']
                file_name = head_dict['filename']
                # recv_path = '/Users/zhiqiangwei/Documents/workspacePython/uploadFile/recv_image/'.format(file_name)

                # file_path = os.path.normpath(
                #     "/Users/zhiqiangwei/Documents/workspacePython/uploadFile/recv_image/")
                # file_path = file_path + "/" + file_name
                file_path = generateErrorImagePath(file_name)
                print(file_path)

                recv_size = 0
                recv_data = 0
                with open(file_path, 'wb') as f:
                    while file_size > 0:
                        if(file_size >= 2048):
                            recv_data = new_socket.recv(2048)
                        else:
                            recv_data = new_socket.recv(file_size)
                        f.write(recv_data)
                        recv_size = len(recv_data)
                        file_size -= recv_size
                    else:
                        print('recvsize:%s filesize:%s' %
                              (recv_size, file_size))

        except Exception:
            break


def main():
    print("main")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 9982))
    server_socket.listen(128)

    while(True):
        # 阻塞等待
        new_connect_socket, client_addr = server_socket.accept()
        print("after blocking")

        # 新的连接处理
        handle_request(new_connect_socket)

    # 关闭套接字
    new_connect_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
