import os
import socket
import json
import struct
import time

import file_handler as fh
import config as cfg
fh = fh.FileHandler()

def main():
    # print(cfg.const.server_ip)
    # return ;
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((cfg.const.SERVER_IP, cfg.const.SERVER_PORT))

    i = 0
    while(i<100):
        i+=1
        file_name = fh.generateErrorSendImagePath( str.format("%d.jpg" %(i)) )
        # print('file_name=%s' %(file_name))
        if( not os.path.isfile(file_name) ):
            print('file:%s is not exists' %file_name)
            break
        else:
            file_size = os.path.getsize(file_name)

        # print('ready send file %s' %file_name)
        # 发送的数据 dict->json->bytes
        head_dic={'cmd':cfg.const.UPLOAD_SCREEN_SHOT, 'filename':os.path.basename(file_name), 'filesize':file_size}
        # print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding='utf-8')

        # 先发送数据长度, 再发送数据
        head_struct = struct.pack('i', len(head_json_bytes))
        client_socket.send(head_struct)
        client_socket.send(head_json_bytes)

        send_size = 0
        t1 = time.time()
        with open(file_name, 'rb') as f:
            while head_dic['filesize'] >= cfg.const.TCP_SEND_SIZE:
                content = f.read(cfg.const.TCP_SEND_SIZE)
                client_socket.send(content)
                head_dic['filesize'] -= len(content)
            else:
                content = f.read(head_dic['filesize'])
                client_socket.send(content)
                head_dic['filesize'] -= len(content)
                
                if(head_dic['filesize'] == 0):
                    # 首先获取长度
                    head_struct = client_socket.recv(4)
                    if not head_struct:
                        break

                    head_len = struct.unpack('i', head_struct)[0]
                    head_json = client_socket.recv(head_len).decode('utf-8')
                    head_dict = json.loads(head_json)

                    print(head_dict)
                    cmd = head_dict['cmd']
                    if cmd == cfg.const.UPLOAD_SCREEN_SHOT_FINISH:
                        print("the server file address=%s" %(head_dict['serverpath']))
                    else:
                        print("can't receive response to server path from server")
            t2 = time.time()

        # print("consume time=%ld" %(t2-t1))

    client_socket.close()

if __name__ == '__main__':
    main()