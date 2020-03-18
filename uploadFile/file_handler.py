class FileHandler:
    def getCurrentDir(self):
        return os.getcwd();

    def getErrorImageDir(self):
        error_image_dir = os.path.join(os.getcwd(), "recv_image")
        if not os.path.exists(error_image_dir):
            os.makedirs(error_image_dir)
        return error_image_dir;

    def generateErrorImagePath(self, file_name):
        # random_name = 'test_{}_{}'.format(time.strftime(
        #     '%Y_%m_%d_%H_%M_%S'), random.randint(1, 999))
        # report_name = f'{random_name}.html'
        path_file = os.path.join(self.getErrorImageDir(), file_name)
        return path_file
