import re
import time

from addressnet.predict import predict
import pandas as pd
from collections import Counter
from dbhepler.mysqlhelper import DBPipeline
from apscheduler.schedulers.blocking import BlockingScheduler

from excel_re import read_excel
import os
import glob

import setting as setting

total_path = glob.glob(os.path.join('*.xls*'))
product_io = '/Users/loctek/Desktop/loctek/address-net/addressnet/乐仓产品数据2.xlsx'
# product_io = 'C:\\addressnet\\乐仓产品数据(1).xlsx'

product_data = pd.read_excel(product_io, dtype=str)

none_product = []

name_list = setting.ssh_name_list
data_country = setting.data_country
word_number = setting.word_number
champion_name = setting.champion_name


def fun_isdigit(aString):
    try:
        return int(aString)
    except ValueError as e:
        return ''


def function(text):
    if 'OT' in text:
        return 'OTTO'
    elif 'AM' in text:
        return 'AMAZON'
    else:
        return 'OTHER'


def get_country(text):
    if pd.isnull(text):
        return ''
    text = str.upper(text)
    if text in data_country.keys():
        return data_country[text]
    else:
        return text


# PR1206-Ebony
def get_delivery(sku, country):  # 物流方式
    try:
        if int(product_data[product_data.SKU == sku]['is_GLS'].values[0]):
            country_list = product_data[product_data.SKU == sku]['国家'].values[0]
            if 'GLOBAL' in country_list:
                return 'GLS_BIZ_PCL'
            if country in country_list:
                return 'GLS_BIZ_PCL'
        product_size = float(product_data[product_data.SKU == sku]['围长'].values[0])  # 对应SKU的围长
        if country == 'DE' and int(product_size) <= 360:
            return 'DHL_DE_PAKET'
        elif ((country == 'DE' or country == 'AT') and product_size > 360) or (
                (country != 'DE' and country != 'AT') and (product_size > 300)):
            return 'DHL_FRIGHT'
        else:
            return 'DHL_DE_INT_PAKET'
    except:
        if sku not in none_product:
            none_product.append(sku)
        return ''


def get_company(consignee_name, old_company, delivery_style):
    if pd.isnull(old_company):
        old_company = ''
    split_names = re.split(r'[,]', consignee_name)

    champion = ''
    for names in split_names:
        get_split_name = names.split(' ')
        for name in reversed(get_split_name):
            if name in champion_name:
                champion = names
    if old_company:
        champion = str(old_company) + champion
    if champion:
        consignee_name = consignee_name.replace(champion, '')
    if 'DHL' in delivery_style and len(champion) > 61:
        return '||||||||||||||||||||||||||||||', consignee_name
    if 'GLS' in delivery_style and len(champion) > 41:
        return '||||||||||||||||||||||||||||||', consignee_name
    return champion, consignee_name


def get_email(text):
    if text:
        return text
    else:
        return '/'


def remake_null(text):
    if not pd.isnull(text):
        return text
    else:
        return ' '


def get_street(doorplate_number, street):
    rule = '(.*)' + doorplate_number + '[,]{0,1}$'
    re_street = re.findall(rule, doorplate_number)
    if re_street:
        return re_street[0]
    return street


def clear_comma(street):
    span_front = re.search(r'(,*$)', street).span()
    street = street[:span_front[0]]
    span_behind = re.search(r'(^,*)', street).span()
    street = street[span_behind[1]:]
    comma_word = re.findall(',,', street)
    if comma_word:
        street = street.replace(comma_word[0], ',')
    street += ','
    return street


def get_ez_street(street, zip_code, consignee_company, city, doorplate):
    street = clear_comma(street)
    print(street)
    ez_street = setting.ez_street
    for word in list(ez_street.keys()):
        capital_words = re.findall(word, street, flags=re.IGNORECASE)
        if capital_words:
            street = street.replace(capital_words[0], ez_street[word])
    zip_code_word = ''
    consignee_company_word = ''
    city_word = ''
    doorplate_word = ''
    # consignee_company += ' '
    print(street, zip_code, consignee_company, city, 123)
    if not pd.isnull(zip_code):
        try:
            zip_code_word = re.findall(zip_code, street, flags=re.IGNORECASE)
            consignee_company_word = re.findall(consignee_company, street, flags=re.IGNORECASE)  # 公司
            city_word = re.findall(city, street, flags=re.IGNORECASE)  # city
            doorplate_word = re.findall(doorplate, street, flags=re.IGNORECASE)  # doorplate
        except:
            pass
    if zip_code_word:
        street = street.replace(zip_code_word[0], '')
    if consignee_company_word:
        # if consignee_company_word[0] != ' ':
        street = street.replace(consignee_company_word[0], '')
    if city_word:
        street = street.replace(city_word[0] + ' ', '')
    if doorplate_word:
        try:
            doorplate_re = doorplate_word[0]
            if '-' in doorplate_word[0]:
                doorplate_re = doorplate_word[0].replace('-', '\-')
            word_split = street.split(',')

            re_sql = doorplate_re + ',(.*)'
            val = re.findall(re_sql, street)
            # if not val:
            # re_s = '[^' + doorplate_re + '](,.*)'
            #  = re.findall(re_sql_2, street)
            mark_mes = val
            mark_mes = mark_mes[0] if mark_mes else ''
        except:
            mark_mes = ''
        consignee_company += mark_mes
        street = street.replace(doorplate_word[0], '')
        street = street.replace(mark_mes, '')
        # print(doorplate_word[0])
        # street = mark_mes
        print(mark_mes)
    consignee_company = consignee_company.replace(doorplate, '')
    street = clear_comma(street)
    consignee_company = clear_comma(consignee_company)
    if consignee_company == ',':
        consignee_company = ''

    if pd.isnull(consignee_company):
        consignee_company = ''
    if len(street) > 35:
        return '||||||||||||||||||||||||||||||', consignee_company
    return street, consignee_company


def get_task():
    db_helper = DBPipeline()  # get DB config
    db_helper.cursor.execute("""select * from view_address_check_bigdate limit 10""")  # run sql
    db_data = db_helper.cursor.fetchall()  # get result
    if not db_data:
        return ''
    fields = [field[0] for field in db_helper.cursor.description]  # get dict key in list
    data_list = [dict(zip(fields, item)) for item in db_data]
    df_data = pd.DataFrame(data_list)
    db_df_data = df_data[
        ['name', 'receiveman', 'countryname', 'city', 'street', 'statezone', 'phone',
         'statezone', 'statezone', 'statezone', 'email', 'company', 'ebname', 'province']]
    db_df_data.columns = setting.ssh_old_columns  # get normal col
    print(db_df_data, 123222)

    db_helper.cursor.close()

    data = db_df_data
    data['Delivery Address Line 1'] = data.apply(lambda x: remake_null(x['Delivery Address Line 1']), axis=1)
    data_dict = dict(data)
    predict_adderss = []
    for i in data_dict['Delivery Address Line 1']:
        predict_adderss.append(i)
    item_list = predict(predict_adderss)  # predict
    tmp_dict = {'flat_number': []}

    b = dict(Counter(data_dict['Order Number']))
    order_tmp_dict = {key: value for key, value in b.items() if value > 1}  # 只展示重复元素
    index = 0
    for order_number in data_dict['Order Number']:
        if order_number in order_tmp_dict.keys():
            order_tmp_dict[order_number] = order_tmp_dict[order_number] - 1
            data_dict['Order Number'][index] = str(data_dict['Order Number'][index]) + str(
                word_number[order_tmp_dict[order_number]])
        tmp_dict['flat_number'].append(
            read_excel(data_dict['Delivery Address Line 1'][index], data_dict['Delivery Country'][index],
                       data_dict['Delivery Postcode'][index]))
        index += 1

    index = 0
    for i in item_list:
        if not tmp_dict['flat_number'][index]:
            if i:
                flat_number = ''
                if 'flat_number' in i.keys():
                    flat_number = i['flat_number']
                    tmp_dict['flat_number'][index] = fun_isdigit(flat_number)
        index += 1
    data_dict.update(tmp_dict)

    data = pd.DataFrame(data_dict)
    data_new = data[
        ['Order Number', 'Delivery Receive Name', 'Delivery Country', 'Delivery Town',
         'Delivery Address Line 1',
         'Delivery Postcode', 'Telephone Number', 'Product Code', 'Quantity', 'flat_number', 'Email Address',
         'Delivery Company', 'ebname', 'province']]
    data_new.columns = setting.ssh_columns
    data_new2 = data_new.reindex(columns=name_list)
    data_new2[['街道2/Street2']] = data_new2[['街道/Street']]
    data_new2[['街道3/Street3']] = data_new2[['收件人公司/Consignee Company']]
    data_new2[['仓库代码/Warehouse Code']] = 'EUKL'
    data_new2[['自动分配仓库']] = 'EUKL'
    data_new2['销售平台/Sales Platform'] = data_new2.apply(lambda x: function(x['参考编号/Reference Code']), axis=1)
    data_new2['收件人国家/Consignee Country'] = data_new2.apply(lambda x: get_country(x['收件人国家/Consignee Country']),
                                                           axis=1)
    data_new2['派送方式/Delivery Style'] = data_new2.apply(
        lambda x: get_delivery(x['SKU1'], x['收件人国家/Consignee Country']), axis=1)
    data_new2['门牌号/Doorplate'] = data_new2.apply(lambda x: get_email(x['门牌号/Doorplate']),
                                                 axis=1)
    try:
        data_new2['收件人公司/Consignee Company'], data_new2['街道/Street'] = zip(*data_new2.apply(
            lambda x: get_company(x['街道/Street'], x['收件人公司/Consignee Company'], x['派送方式/Delivery Style']),
            axis=1))
        # data_new2['街道/Street'] = data_new2.apply(lambda x: get_street(x['门牌号/Doorplate'], x['街道/Street']),
        #                                          axis=1)
        data_new2['街道/Street'], data_new2['收件人公司/Consignee Company'] = zip(*data_new2.apply(
            lambda x: get_ez_street(x['街道/Street'], x['邮编/Zip Code'],
                                    x['收件人公司/Consignee Company'],
                                    x['城市/City'], x['门牌号/Doorplate']
                                    ), axis=1))
    except Exception as error:
        print(error)
    # --- new ---
    data_new2.to_excel('asdasd.xls', index=False)
    data_clear = data_new2[[
        '参考编号/Reference Code', 'ebname', '街道2/Street2', '城市/City', '邮编/Zip Code', 'province',
        '收件人国家/Consignee Country', '收件人电话/Consignee Phone', '收件人Email/Consignee Email',
        '街道3/Street3', '街道/Street', '门牌号/Doorplate', '收件人公司/Consignee Company'
    ]]
    data_clear.columns = setting.columns_to_dict
    data_clear = data_clear.to_dict(orient='records')
    for item in data_clear:
        print(item)
        DBPipeline().process_item(item)
    return 'ok'
    # data_new2.to_excel('asdasd.xls', index=False)


if __name__ == "__main__":
    get_task()
    scheduler = BlockingScheduler()
    scheduler.add_job(get_task, 'interval', hours=8)
    scheduler.start()
