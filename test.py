import pymysql
import threading
from queue import Queue


def ratio(data):
    info_data = []
    for it in range(0, len(data) - len(data) // 2):
        a = [d.get('data', 0) for d in data]
        qw = a.index(data[it]['data'], len(data) // 2, len(data))
        qe = data[qw]['saleamount'] / data[it]['saleamount']
        args = {
            'dates': data[qw]['data'],
            'global_saleamount': data[qw]['saleamount'],
            'global_site_saleamount': data[it]['saleamount'],
            'ratio': "%.2f%%" % (qe * 100),
            'site': data[qw]['site']
        }
        info_data.append(args)
    return info_data


# 全球独立站占比
def Global_site(start_time, end_time, backValue):
    connect = pymysql.connect(
        host='old-db-abs56.mysql.database.azure.com',
        port=3306,
        user='loctekroot@old-db-abs56',
        password='FHY7LEVv*G*#%K&@',
        database='abs3',
        charset='utf8'
    )
    cursor = connect.cursor()
    # print('全球')
    global_sum_sql = '''SELECT yyyymm,sum( saleamount ) AS saleamount FROM( SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,sum(a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfodetail a LEFT JOIN orderinfo o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.paydate >= '{}' AND o.paydate <= '{}' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,sum( a.num *( ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfohistorydetail a LEFT JOIN orderinfohistory o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.paydate >= '{}' AND o.paydate <= '{}' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) ) a GROUP BY a.yyyymm UNION SELECT yyyymm,sum( saleamount ) AS saleamount FROM ( SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm, sum( a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfodetail a LEFT JOIN orderinfo o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.sourcename IN ( 'FlexiSpot', 'FlexiSpotUSOffline', 'Fleximounts', 'FlexiSpotCAN', 'FlexiSpotDE', 'FlexiSpotUK', 'FlexiSpotFR', 'FlexiSpotJP', 'FlexiSpotJP02','FlexispotIT', 'FlexispotES' ) AND o.paydate >= '{}' AND o.paydate <= '{}' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm, sum(a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfohistorydetail a LEFT JOIN orderinfohistory o ON a.orderinfo = o.id  LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.sourcename IN ('FlexiSpot', 'FlexiSpotUSOffline', 'Fleximounts', 'FlexiSpotCAN', 'FlexiSpotDE', 'FlexiSpotUK', 'FlexiSpotFR', 'FlexiSpotJP', 'FlexiSpotJP02','FlexispotIT', 'FlexispotES') AND o.paydate >= '{}' AND o.paydate <= '{}' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 )) a GROUP BY a.yyyymm '''.format(
        start_time, end_time, start_time, end_time, start_time, end_time, start_time, end_time)
    cursor.execute(global_sum_sql)
    # 获取所有的数据
    global_sum = cursor.fetchall()
    data = []
    for it in global_sum:
        args = {
            'data': it[0],
            'saleamount': it[1],
            'site': '全球'
        }
        data.append(args)
    datas = ratio(data)
    connect.close()
    backValue.put(datas)


# 美国独立站占比
def Us_site(start_time, end_time, backValue):
    connect = pymysql.connect(
        host='old-db-abs56.mysql.database.azure.com',
        port=3306,
        user='loctekroot@old-db-abs56',
        password='FHY7LEVv*G*#%K&@',
        database='abs3',
        charset='utf8'
    )
    cursor = connect.cursor()
    # print('美国')
    global_sum_sql = """SELECT yyyymm,sum( saleamount ) AS saleamount FROM( SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,sum(a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfodetail a LEFT JOIN orderinfo o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'US' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,sum( a.num *( ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfohistorydetail a LEFT JOIN orderinfohistory o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'US' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) ) a GROUP BY a.yyyymm UNION SELECT yyyymm,sum( saleamount ) AS saleamount FROM ( SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm, sum( a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfodetail a LEFT JOIN orderinfo o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.sourcename IN ( 'FlexiSpot', 'FlexiSpotUSOffline', 'Fleximounts' ) AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'US' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm, sum(a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfohistorydetail a LEFT JOIN orderinfohistory o ON a.orderinfo = o.id  LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.sourcename IN ( 'FlexiSpot', 'FlexiSpotUSOffline', 'Fleximounts') AND o.paydate >= '{}' AND o.paydate <='{}' AND o.sitecode = 'US' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 )) a GROUP BY a.yyyymm 
    """.format(start_time, end_time, start_time, end_time, start_time, end_time, start_time, end_time)

    cursor.execute(global_sum_sql)
    global_sum = cursor.fetchall()
    data = []
    for it in global_sum:
        args = {
            'data': it[0],
            'saleamount': it[1],
            'site': '美国'
        }
        data.append(args)
    datas = ratio(data)
    connect.close()
    backValue.put(datas)


# 欧洲独立站占比
def Eu_site(start_time, end_time, backValue):
    connect = pymysql.connect(
        host='old-db-abs56.mysql.database.azure.com',
        port=3306,
        user='loctekroot@old-db-abs56',
        password='FHY7LEVv*G*#%K&@',
        database='abs3',
        charset='utf8'
    )
    cursor = connect.cursor()
    # print('欧洲')
    global_sum_sql = """SELECT yyyymm,sum( saleamount ) AS saleamount FROM( SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,sum(a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfodetail a LEFT JOIN orderinfo o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'EU' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,sum( a.num *( ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfohistorydetail a LEFT JOIN orderinfohistory o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'EU' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) ) a GROUP BY a.yyyymm UNION SELECT yyyymm,sum( saleamount ) AS saleamount FROM ( SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm, sum( a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfodetail a LEFT JOIN orderinfo o ON a.orderinfo = o.id LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.sourcename IN ( 'FlexiSpotCAN', 'FlexiSpotDE', 'FlexiSpotUK','FlexiSpotFR',  'FlexispotIT', 'FlexispotES' ) AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'EU' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION SELECT LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm, sum(a.num *(ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount FROM orderinfohistorydetail a LEFT JOIN orderinfohistory o ON a.orderinfo = o.id  LEFT JOIN product p ON p.id = a.productid WHERE 1 = 1 AND o.isactive = '1' AND o.state IN ( '1', '10', '11', '21', '41', '20' ) AND o.isallmatch = '1' AND o.sourcename IN ('FlexiSpotCAN', 'FlexiSpotDE', 'FlexiSpotUK', 'FlexiSpotFR','FlexispotIT', 'FlexispotES') AND o.paydate >= '{}' AND o.paydate <= '{}' AND o.sitecode = 'EU' GROUP BY LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 )) a GROUP BY a.yyyymm
    """.format(start_time, end_time, start_time, end_time, start_time, end_time, start_time, end_time)

    cursor.execute(global_sum_sql)
    global_sum = cursor.fetchall()
    data = []
    for it in global_sum:
        args = {
            'data': it[0],
            'saleamount': it[1],
            'site': '欧洲'
        }
        data.append(args)
    datas = ratio(data)
    connect.close()
    backValue.put(datas)


# 日本独立站占比
def Jp_site(start_time, end_time, backValue):
    connect = pymysql.connect(
        host='old-db-abs56.mysql.database.azure.com',
        port=3306,
        user='loctekroot@old-db-abs56',
        password='FHY7LEVv*G*#%K&@',
        database='abs3',
        charset='utf8'
    )

    # 获取游标对象
    cursor = connect.cursor()
    # print('日本')
    global_sum_sql = """SELECT
        yyyymm,
        sum( saleamount ) AS saleamount 
        FROM
            (
            SELECT LEFT
                ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,
                sum(
                    a.num *(
                    ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount 
            FROM
                orderinfodetail a
                LEFT JOIN orderinfo o ON a.orderinfo = o.id
                LEFT JOIN product p ON p.id = a.productid 
            WHERE
                1 = 1 
                AND o.isactive = '1' 
                AND o.state IN ( '1', '10', '11', '21', '41', '20' ) 
                AND o.isallmatch = '1' 
                AND o.sitecode = 'JP'
                AND o.paydate >= '{}'
                AND o.paydate <= '{}'
            GROUP BY
                LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION
            SELECT LEFT
                ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,
                sum(
                    a.num *(
                    ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount 
            FROM
                orderinfohistorydetail a
                LEFT JOIN orderinfohistory o ON a.orderinfo = o.id
                LEFT JOIN product p ON p.id = a.productid 
            WHERE
                1 = 1 
                AND o.isactive = '1' 
                AND o.state IN ( '1', '10', '11', '21', '41', '20' ) 
                AND o.isallmatch = '1'  
                AND o.sitecode = 'JP'
                AND o.paydate >=  '{}'
                AND o.paydate <= '{}' 
            GROUP BY
                LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) 
                ) a 
            GROUP BY
                a.yyyymm UNION
        SELECT
            yyyymm,
            sum( saleamount ) AS saleamount 
        FROM
            (
            SELECT LEFT
                ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,
                sum(
                    a.num *(
                    ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount 
            FROM
                orderinfodetail a
                LEFT JOIN orderinfo o ON a.orderinfo = o.id
                LEFT JOIN product p ON p.id = a.productid 
            WHERE
                1 = 1 
                AND o.isactive = '1' 
                AND o.state IN ( '1', '10', '11', '21', '41', '20' ) 
                AND o.isallmatch = '1' 
                AND o.sitecode = 'JP'
                AND o.sourcename IN ( 'FlexiSpotJP','FlexiSpotJP02') 
                AND o.paydate >= '{}'
                AND o.paydate <= '{}'
            GROUP BY
                LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) UNION
            SELECT LEFT
                ( date_format( o.paydate, '%Y-%m-%d' ), 7 ) AS yyyymm,
                sum(  
                    a.num *(
                    ifnull( a.price, 0 )+ ifnull( a.expprice, 0 ))) AS saleamount 
            FROM
                orderinfohistorydetail a
                LEFT JOIN orderinfohistory o ON a.orderinfo = o.id
                LEFT JOIN product p ON p.id = a.productid 
            WHERE
                1 = 1 
                AND o.isactive = '1' 
                AND o.state IN ( '1', '10', '11', '21', '41', '20' ) 
                AND o.isallmatch = '1' 
                AND o.sitecode = 'JP'
                AND o.sourcename IN ('FlexiSpotJP','FlexiSpotJP02') 
                AND o.paydate >= '{}'
                AND o.paydate <= '{}'
            GROUP BY
            LEFT ( date_format( o.paydate, '%Y-%m-%d' ), 7 )) a 
        GROUP BY
            a.yyyymm 
    """.format(start_time, end_time, start_time, end_time, start_time, end_time, start_time, end_time)

    cursor.execute(global_sum_sql)
    # 获取所有的数据
    global_sum = cursor.fetchall()
    data = []
    for it in global_sum:
        args = {
            'data': it[0],
            'saleamount': it[1],
            'site': '日本'
        }
        data.append(args)
    datas = ratio(data)
    # print(global_sum)

    # 关闭数据库连接
    connect.close()
    backValue.put(datas)


def main(start_time, end_time):
    backValue = Queue()
    threads = [threading.Thread(target=Global_site, args=[start_time, end_time, backValue]),
               threading.Thread(target=Us_site, args=[start_time, end_time, backValue]),
               threading.Thread(target=Eu_site, args=[start_time, end_time, backValue]),
               threading.Thread(target=Jp_site, args=[start_time, end_time, backValue])]
    for t in threads:
        # 启动线程
        t.start()
    results = []
    for _ in range(4):
        results.append(backValue.get())
    # print(results)
    return results


if __name__ == '__main__':
    main('2021-01-01 00:00:00', '2021-12-02 23:59:59')
