import threading
import time

class Mythread(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self)
        self.name = threadName

    def run(self):
        self.sign()
        
    def sign(self):
        """i am signing"""
        for i in range(5):
            time.sleep(1)
            print("{} i am signing {}".format(self.name, i))

def main():
    t1 = Mythread("subthrad1")
    t1.start()

if __name__ == '__main__':
    main()