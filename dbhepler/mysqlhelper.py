import datetime
from logging import log

import pymysql


class DBPipeline:
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='old-db-abs56.mysql.database.azure.com',
            port=3306,
            db='abs3',
            user='loctekroot@old-db-abs56',
            passwd='FHY7LEVv*G*#%K&@',
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def get_message(self):
        self.cursor.execute("""select * from view_address_check_bigdate""")
        data = self.cursor.fetchall()
        print(data)
        print(1)
        return data

    def process_item(self, item):
        self.cursor.execute(
            """select * from order_check_address where org_name = %s""",
            (item['org_name']))
        repetition = self.cursor.fetchone()
        if repetition:
            return 'have data'
        try:
            self.cursor.execute(
                """insert into order_check_address(org_name, org_ebname, org_street, org_city, org_receivezip, org_province,
                 org_countryname, org_phone, org_email, org_company,new_address1, new_address4, new_company, createtime)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['org_name'],
                 item['org_ebname'],
                 item['org_street'],
                 item['org_city'],
                 item['org_receivezip'],
                 item['org_province'],
                 item['org_countryname'],
                 item['org_phone'],
                 item['org_email'],
                 item['org_company'],
                 item['new_address1'],
                 item['new_address4'],
                 item['new_company'],
                 datetime.datetime.now()
                 )
            )
            self.connect.commit()
            self.cursor.execute(
                """update orderinfo_bigdata_test
                   SET fedexaddressvalidate = 'Y'
                   WHERE name = %s
                """, (item['org_name']))
            self.connect.commit()
            self.cursor.close()
        except Exception as error:
            print(error)
            # 出现错误时打印错误日志
            pass
        return item
