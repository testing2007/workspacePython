import os
import socket
import json
import struct
import time

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("47.93.202.254", 9000))

    i = 0
    while(i<100):
        i+=1
        file_name = str.format("/Users/zhiqiangwei/Documents/workspacePython/uploadFile/image/%d.jpg" %(i))
        if( not os.path.isfile(file_name) ):
            print('file:%s is not exists' %file_name)
            break
        else:
            file_size = os.path.getsize(file_name)

        print('ready send file %s' %file_name)
        # continue

        # 发送的数据 dict->json->bytes
        head_dic={'cmd':'UPLOAD_SCREEN_SHOT', 'filename':os.path.basename(file_name), 'filesize':file_size}
        print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding='utf-8')

        # 先发送数据长度, 再发送数据
        head_struct = struct.pack('i', len(head_json_bytes))
        client_socket.send(head_struct)
        client_socket.send(head_json_bytes)

        send_size = 0
        t1 = time.time()
        with open(file_name, 'rb') as f:
            while head_dic['filesize'] >= 2048:
                content = f.read(2048)
                client_socket.send(content)
                head_dic['filesize'] -= len(content)
            else:
                content = f.read(head_dic['filesize'])
                client_socket.send(content)
                head_dic['filesize'] -= len(content)
            t2 = time.time()

        print("consume time=%ld" %(t2-t1))

    client_socket.close()

if __name__ == '__main__':
    # str ='123'
    # print('str content=', str[0:len(str)])
    
    main()