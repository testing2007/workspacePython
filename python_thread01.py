import threading
import time


def sign():
    """i am signing"""
    for i in range(5):
        time.sleep(1)
        print("i am signing {}".format(i))

def dance():
    """i am dancing"""
    for i in range(5):
        time.sleep(1)
        print("i am dancing {}".format(i))


def main():
    t1 = threading.Thread(target=sign)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()



if __name__ == '__main__':
    main()