# -*-coding:utf-8-*-
from webService import start_server
from userParser import user_parser

def main():
    print('——'*20)
    print('【1】启动查询服务')
    print('【2】收集当前飞球用户信息')
    select = input('请选择功能：')
    if select == '1':
        start_server()
    if select == '2':
        user_parser()
    else:
        print('非法输入')
        return

if __name__ == '__main__':
    while 1:
        main()
