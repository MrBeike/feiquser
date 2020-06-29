# -*-coding:utf-8
import time
from wsgiref.simple_server import make_server
from DataBase import Dict2DB as DB

# TODO 与数据库相关操作解耦
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    query_string = environ['QUERY_STRING']   
    prefix = '114'
    query_list = [x.split('=') for x  in query_string.split('&')]
    keyword_get = query_list[0][1].replace(prefix,'')
    ip_get = query_list[1][1]
    keyword_unicode = keyword_get.encode('raw_unicode_escape')
    keyword  = keyword_unicode.decode('gbk')
    black_list = ['11.65.13.172']
    date_time =time.strftime("%Y-%m-%d-%H-%M")
    print(ip_get,keyword)
    with open('log.txt','a+',encoding='utf-8') as f:
        f.write(f'{date_time}:{ip_get}:{keyword}\n')
    if ip_get in black_list:
        return ['寒谭渡鹤影，冷月葬花魂'.encode('utf-8')]
    if keyword == '':
        return ['[未输入关键词]江南无所有，聊赠一支春'.encode('utf-8')]
    result = DB.read_data('feiq.db',keyword)
    # result -> list[tuple(NikeName,HostName,MakeName,IP)]
    if result:
        person_info_list = []
        for item in result:
            person_info = ' '.join(item)
            person_info_list.append(person_info)
        person_infos = '\n'.join(person_info_list)    
        print(person_infos)
        response = person_infos.encode('utf-8')
        return [response]
    else:
        response = '[信息未收录]莫愁前路无知己，天下谁人不识君。'.encode('utf-8')
        return[response]

def start_server():
    # 创建一个服务器，IP地址为空，端口是9999，处理函数是application:
    httpd = make_server('0.0.0.0', 9999, application)
    # 开始监听HTTP请求:
    httpd.serve_forever()
