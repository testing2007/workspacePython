import os
import socket
import json
import struct
import time

import file_handler as fh
import config as cfg
fh = fh.FileHandler()


class ClientTCPSocket:
    def __init__(self, sip, sport):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = sip
        self.port = sport
        self.upload_dict = {}
    
    def _createSocket(self):
        if (self.socket is None):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self.socket
        
    def connect(self):
        self.socket.connect((self.ip, self.port))
    
    def close(self):
        self.socket.close()
    
    def uploadErrorImage(self, local_file_path):
           # print('file_name=%s' %(file_name))
        if( not os.path.isfile(local_file_path) ):
            print('file:%s is not exists' %local_file_path)
            return
        else:
            file_size = os.path.getsize(local_file_path)

        # print('ready send file %s' %file_name)
        # 发送的数据 dict->json->bytes
        head_dic={'cmd':cfg.const.UPLOAD_SCREEN_SHOT, 'filename':os.path.basename(local_file_path), 'filesize':file_size}
        # print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding='utf-8')

        # 先发送数据长度, 再发送数据
        head_struct = struct.pack('i', len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.send(head_json_bytes)

        send_size = 0
        t1 = time.time()
        with open(local_file_path, 'rb') as f:
            while head_dic['filesize'] >= cfg.const.TCP_SEND_SIZE:
                content = f.read(cfg.const.TCP_SEND_SIZE)
                self.socket.send(content)
                head_dic['filesize'] -= len(content)
            else:
                content = f.read(head_dic['filesize'])
                self.socket.send(content)
                head_dic['filesize'] -= len(content)
                
                if(head_dic['filesize'] == 0):
                    # 首先获取长度
                    head_struct = self.socket.recv(4)
                    if not head_struct:
                        return 

                    head_len = struct.unpack('i', head_struct)[0]
                    head_json = self.socket.recv(head_len).decode('utf-8')
                    head_dict = json.loads(head_json)

                    print(head_dict)
                    cmd = head_dict['cmd']
                    if cmd == cfg.const.UPLOAD_SCREEN_SHOT_FINISH:
                        print("the server file address=%s" %(head_dict['serverpath']))
                        self.upload_dict[local_file_path] = head_dict['serverpath']
                    else:
                        print("can't receive response to server path from server")
            t2 = time.time()

        # print("consume time=%ld" %(t2-t1))
        
    def get_upload_server_path(self, local_file_path):
        # return self.upload_dict[local_file_path]
        if local_file_path in self.upload_dict:
            return self.upload_dict[local_file_path]
        return None
    

def main():
    # print(cfg.const.server_ip)
    # return ;
    client_socket = ClientTCPSocket(cfg.const.SERVER_IP, cfg.const.SERVER_PORT)
    client_socket.connect()

    i = 0
    while(i<100):
        i+=1
        file_path = fh.generateErrorSendImagePath( str.format("%d.jpg" %(i)) )
        if( not os.path.isfile(file_path) ):
            print('file:%s is not exists' %file_path)
            return
        client_socket.uploadErrorImage(file_path)
        server_path = client_socket.get_upload_server_path(file_path)
        if( server_path ):
            print("server_path="+server_path)

    client_socket.close()

if __name__ == '__main__':
    main()