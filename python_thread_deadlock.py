import threading
import time


g_num = 0 

mutex1 = threading.Lock()
mutex2 = threading.Lock()

def sum1(num):
	global g_num
	mutex1.acquire()
	for i in range(num):
		print("sum1 for before mutex2.acquire() g_num ={}".format(g_num))
		mutex2.acquire()
		print("sum1 for after mutex2.acquire() g_num ={}".format(g_num))
		g_num += 1
		mutex2.release()
	mutex1.release()
	print("sum1 g_num={}".format(g_num))

def sum2(num):
	global g_num
	mutex2.acquire()
	for i in range(num):
		print("sum2 for before mutex1.acquire() g_num ={}".format(g_num))
		mutex1.acquire()
		print("sum2 for after mutex1.acquire() g_num ={}".format(g_num))
		g_num += 1
		mutex1.release()
	mutex2.release()
	print("sum2 g_num={}".format(g_num))
	
def main():
	t1 = threading.Thread(target=sum1, args=(100000,))
	t2 = threading.Thread(target=sum2, args=(100000,))
	t1.start()
	t2.start()
		
	time.sleep(2)

	print("main thread g_num=%d" % g_num)


if __name__ == "__main__":
	main()