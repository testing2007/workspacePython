import os
import socket
import re
import json
import urllib.request

def downloadImage(imageURL):
    res = re.match(r"/[^/]*", imageURL) #(\.)+.*
    res = imageURL.split("/")
    localImageName = res[res.__len__()-1]
    print(localImageName)
    imageURLPath = "https://image.suning.cn/" + imageURL
    print("imageURLPath=",imageURLPath)
    localPath = "./image/"+localImageName 
    print("localPath=",localPath)
    with open(localPath, "wb") as f:
            res = urllib.request.urlopen(imageURLPath)
            try:
                while True:
                    content = res.read()
                    if content.__len__() == 0:
                        break;
                    f.write(content)
            except Exception as ex:
                print(ex)
                
def extractFileName(httpRequestData):
    # info = "GET /index.html HTTP/1.1"
    res = re.match(r"[^ ]* /([^ ]*)", httpRequestData.decode("UTF-8")) #小写utf-8
    if res[1] == '':
        print("is empty")
    else:
        print("is not empty, the file=", res[1])
    return res[1]

def extractImageURL(jsonContent):
    jsonObj = json.loads(jsonContent)

    imgList = list()

    for itemData in jsonObj["data"]:
        try:
            itemTagArr = itemData["tag"]
            for itemTag in itemTagArr:
                if (itemTag):
                    picUrl = itemTag["picUrl"]
                    if(picUrl.__len__()>0):
                        imgList.append(picUrl)
                        print(itemTag["picUrl"])
        except Exception as ex:
            print(ex)
    
    return imgList

def handleRequest(newSocket):
    while True:
        httpRequestData = newSocket.recv(1024)
        print(httpRequestData)
        if(httpRequestData):
            fileName = extractFileName(httpRequestData)
            #打开文件
            try:
                f = open(fileName)
                jsonContent = ''
                while True: 
                    content = f.read(1024)
                    if content.__len__() == 0:
                        imgList = extractImageURL(jsonContent)

                        for itemImageURL in imgList:
                            downloadImage(itemImageURL)

                        break
                    # print(content)
                    jsonContent += content
            except Exception as ex:
                print(ex)
            finally:
                f.close()
        else:
            newSocket.close()
            break

def main():
    tcpListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpListenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpListenSocket.bind(("", 8081))
    tcpListenSocket.listen(128)

    #阻塞等待
    newConnectSocket, clientAddr = tcpListenSocket.accept()

    #新的连接处理
    handleRequest(newConnectSocket)


if __name__ == "__main__":
    main()

    # info = "GET /index.html HTTP/1.1"
    # res = re.match(r"[^ ]* /([^ ]*)", info)
    # if res[1] == '':
    #     print("is empty")
    # else:
    #     print("is not empty, the file=", res[1])
    
    # info = "/uimg/cms/img/156258751845678593.jpg"
    # res = re.match(r"/[^/]*", info) #(\.)+.*
    # res = info.split("/")
    # print(res[res.__len__()-1])
