import requests
import re
import pymysql
import random
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
}


def not_empty(s):
    list_s = []
    for i in s:
        list_s.append(''.join(i.strip()))
    return list_s


# 合并列表里的元素
def merge(list_s):
    k = 0
    a_str = ' '
    while k < len(list_s):
        a_str = a_str + str(list_s[k])
        k += 1
    return a_str.replace('\r', '').replace('\n', '').replace('\t', '')


# def req_ip():
#     pool = []
#     myclient = pymongo.MongoClient("mongodb://40.73.115.215:27017/")
#     mydb = myclient["proxy_pool"]
#     mydb.authenticate("proxy", "Loctek#2020")
#     mycol = mydb["proxy"]
#     data = mycol.find({},{'_id':0,'name':1})
#     # 读取数据
#     data = mycol.find({},{'_id':0,'name':1})
#     for i in data:
#         pool.append(i['name'])
#     return pool

pool = req_ip()
ips = random.choice(pool)
proxies = {
    "http": "http://{}".format(ips),
    "https": "https://{}".format(ips),
}
print('、、、、、、、、、、、  代理 IP   ', proxies)

try:
    for i in range(1000):
        url = 'https://book.douban.com/tag/%E8%80%BD%E7%BE%8E?start={}&type=T'.format(i)
        print(url)
        res = requests.get(url, headers=headers, proxies=proxies)
        house = etree.HTML(res.text).xpath('//*[@id="content"]/h1/text()')
        url_link = merge(
            not_empty(etree.HTML(res.text).xpath('//*[@id="subject_list"]/ul/li[1]/div[2]/h2/a/@href')))  # 每个数据链接
        title = merge(
            not_empty(etree.HTML(res.text).xpath('//*[@id="subject_list"]/ul/li[1]/div[2]/h2/a/text()')))  # 名字
        conn = mdb.connect(host='east2-vm-database.mysql.database.chinacloudapi.cn', port=3306,
                           user='loctek@east2-vm-database',
                           passwd='vHhV8DfsSy2ZxA', db='movie', charset='utf8')
        cursor = conn.cursor()
        sqls = '''select * from echo_loctek_books where title = %s'''
        cursor.execute(sqls, title)
        result = cursor.fetchall()
        resultss = len(result)
        if resultss > 0:
            print('>>>>>>>> 数 据 已 存 在  ---------------------跳 过 以 下 请 求---------------------------------')
            pass
        else:
            print(url_link)
            print(title)
            req = requests.get(url_link, headers=headers, proxies=proxies)
            title_list = etree.HTML(req.text).xpath('//*[@id="info"]//text()')
            # 图片
            try:
                img = etree.HTML(req.text).xpath('//*[@id="mainpic"]/a/img/@src')[0]
            except:
                img = ''
            # 评分
            try:
                shar = etree.HTML(req.text).xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
            except:
                shar = ''
            txt = merge(not_empty(title_list))
            # 作者
            try:
                types = re.findall("作者:(.*?)出版社", txt)[0]
            except:
                types = ''
            # 出版社
            try:
                try:
                    press = re.findall("出版社:(.*?)原作名", txt)
                except:
                    press = re.findall("出版社:(.*?)出品方", txt)
                try:
                    press = re.findall("出版社:(.*?)出版年", txt)
                except:
                    press = re.findall("出版社:(.*?)页数", txt)
                if press == []:
                    press = re.findall("出版社:(.*?)副标题", txt)
                if press == []:
                    press = re.findall("出版社:(.*?)装帧", txt)
            except:
                press = ['']
            if press == []:
                press = ['']
            print(press)
            # # 出版年
            try:
                try:
                    sketchy = re.findall("出版年:(.*?)页数", txt)[0]
                except:
                    sketchy = re.findall("出版年:(.*?)定价", txt)[0]
            except:
                sketchy = ''
            try:
                label = etree.HTML(req.text).xpath('//*[@id="db-tags-section"]/div/span/a/text()')
            except:
                label = ''
            arrest = "/".join(label)
            cone = "".join(house)[7:]
            spare = cone + "/" + arrest
            # 内容简介
            theory = etree.HTML(req.text).xpath('//*[@id="link-report"]/div[1]/div/p/text()')
            if theory == []:
                theory = etree.HTML(req.text).xpath('//*[@id="link-report"]/span[1]/div/p/text()')
            # 作者简介
            play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/div/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/span[1]/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/span[1]/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//div[@class="indent "]/span[@class="short"]/div/p/text()')
            content = merge(not_empty(theory))  # 内容简介
            author = merge(not_empty((play)))  # 作者简介
            print(types)
            print(sketchy)
            print(content)
            print(author)
            print(spare)
            source = '豆瓣书籍'
            conn = mdb.connect(host='east2-vm-database.mysql.database.chinacloudapi.cn', port=3306,
                               user='loctek@east2-vm-database',
                               passwd='vHhV8DfsSy2ZxA', db='movie', charset='utf8')
            cursor = conn.cursor()
            sql = 'insert into echo_loctek_books(title, img, content, author, brief, rate, be_on, source, cate, press) value("{}","{}","{}","{}","{}","{}","{}","{}","{}", "{}")'.format(
                title, img, mdb.escape_string(content), types, mdb.escape_string(author), shar, sketchy, source, spare,
                press[0])
            # 提交sql语句，映射到数据库中。
            print(sql)
            cursor.execute(sql)
            conn.commit()
            # 关闭数据库连接
            conn.close()
except Exception as e:
    print(e)
