import os


class FileHandler(object):
    def getCurrentDir(self):
        return os.getcwd()

    def getErrorImageDir(self, folder_name):
        error_image_dir = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(error_image_dir):
            os.makedirs(error_image_dir)
        return error_image_dir

    def generateErrorRecvImagePath(self, file_name):
        path_file = os.path.join(self.getErrorImageDir("recv_image"), file_name)
        return path_file
    
    def generateErrorSendImagePath(self, file_name):
        path_file = os.path.join(self.getErrorImageDir("send_image"), file_name)
        return path_file

if __name__ == '__main__':
    a = FileHandler()
    print(a.getErrorImageDir())
    print(a.getCurrentDir())
    print(a.generateErrorImagePath("11.jpg"))
