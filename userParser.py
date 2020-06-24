# -*-coding:utf-8-*-
import os,time,configparser,subprocess

from DataBase import Dict2DB as DB 

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
 

# FIXME row_id change?


def xml_geter():
    '''
    通过飞秋命令行API导出在线好友信息.
    1.读取飞秋配置文件获取飞秋运行路径和工作文件夹
    2.通过命令行获取飞秋在线好友信息（{datetime}.xml）
    '''
    appdata_path = os.getenv('APPDATA')  #C:\Users\XXX\AppData\Roaming
    feiq_ini_path = os.path.join(appdata_path , 'feiq','feiq.ini')
    config = configparser.ConfigParser()
    config.read(feiq_ini_path)
    # 获取feiq工作文件夹(通过命令行获取的xml文件在工作文件夹下ParamFile子文件夹里)
    work_directory = config['FeiQ']['WorkDirectory']
    xml_path = os.path.join(work_directory,'feiq','ParamFile')
    # 获取feiq.exe程序路径
    feiq_exe_path = config['FeiQConfigInfo']['FeiqRunExePath']
    datetime = time.strftime("%Y-%m-%d-%H-%M")
    command = rf"{feiq_exe_path} \userxml:{datetime}.xml"
    # 利用cmd命令导出飞秋好友，生成xml文件
    out = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    xml_file = os.path.join(xml_path,f'{datetime}.xml')
    print(xml_file)
    time.sleep(5)
    if os.path.exists(xml_file):
        print('xml文件获取成功')
        return xml_file
    else:
        print('get user from feiq failed')
        return False

def xml_convert(xml_file):
    '''
    解决xml文件gbk编码在python里报错的问题.
    1.改变文件编码
    2.替换xml中编码标识gb2312 -> utf-8
    '''
    print('开始文件转换。')
    with open(xml_file) as f:
        content = f.read()
        content.encode(encoding='utf-8')
        content = content.replace('gb2312','utf-8')
    with open(xml_file,'w',encoding='utf-8') as f:
        f.write(content)
    print('文件转换完成。')

def xml_parser(xml_file):
    '''
    解析xml文件内容，并将获取到的用户信息存入数据库（dict->database）.
    1.通过xml解析xml文件内用户信息部分。（<Buddy>）
    2.将信息转换并存入数据库。（item.attrib ->dict）
    '''
    print('开始文件解析')
    content = ET.parse(xml_file)
    root = content.getroot()
    for item in root:
        buddy_content = item.attrib
        key_list = []
        value_list = []
        for key,value in buddy_content.items():
            key_list.append(key)
            value_list.append(value)
        DB('feiq.db',key_list,value_list)
    print(f'解析完毕，共解析{len(root)}条信息')

def user_parser():
    while 1:
        xml_file = xml_geter()
        i = 0
        i += 1
        count_entry_before = DB.count_entry('feiq.db')[0][0]
        if xml_file:
            xml_convert(xml_file)
            xml_parser(xml_file)
            count_entry = DB.count_entry('feiq.db')[0][0]
            diff = count_entry - count_entry_before
            print(f'数据库内共有{count_entry}条记录,本次新增{diff}条记录')
            return
        elif i >= 3:
            print('尝试获取用户xml文件失败，请检查网络并重试。')
            return

if __name__ == '__main__':
    user_parser()