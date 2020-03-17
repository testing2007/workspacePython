# 方式一：
# import common 
# 方式二/三：
from common import bHandleFinished

# bHandleFinished = True
# print("global value=", bHandleFinished)

def modifyValue():
    # 方式一：
    # common.bHandleFinished = True
    # print("modify value=", common.bHandleFinished)

    # 方式二：
    # bHandleFinished = True
    # print("modify value=", bHandleFinished)
    
    # 方式三：
    # global bHandleFinished
    bHandleFinished = True
    print("modify value=", bHandleFinished)
 


def fetchValue():
    # 方式一：
    # print("fetch value=", common.bHandleFinished)

    # 方式二/三：
    print("fetch value=", bHandleFinished)

def main():
    modifyValue()
    fetchValue()


if __name__ == "__main__":
    main()