
import os

def main():
    print('单引号字符串')

    print("双引号字符串")

    foo(5, 10)

    print('1'*10)
    print('字符串连接'+os.getcwd())

    counter = 0
    counter += 1

    foodList = ['apple', 'pander', 'banana']
    for i in foodList:
        print('i am a'+i)

    stringList = 'abcde'
    for i in stringList:
        print('stringList item='+i)
    
def foo(param1, param2):
    '''
    多行注释
    '''
    res = param1+param2
    print("the result is equal to %d", res)
    if res>10:
        print("res>10")
    elif (res>5) and (res<=10):
        print("(res>5) and (res<=10)")
    else:
        print('else')
    return res #单行注释

if __name__ == '__main__':
    main()