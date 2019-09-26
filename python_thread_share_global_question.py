import threading
import time


g_num = 0 
	
def sum1(num):
	global g_num
	for i in range(num):
		g_num += i
	print("sum1 g_num={}".format(g_num))

def sum2(num):
	global g_num
	for i in range(num):
		g_num += 1
	print("sum2 g_num={}".format(g_num))
	
def main():
	t1 = threading.Thread(target=sum1, args=(100,))
	t2 = threading.Thread(target=sum2, args=(100,))
	t1.start()
	t2.start()
		
	time.sleep(2)

	print("main thread g_num=%d" % g_num)

if __name__ == "__main__":
	main()