import pandas as pd

import setting as setting

total_path = glob.glob(os.path.join('*.xls*'))
product_io = '/Users/loctek/Downloads/乐仓产品数据.xlsx'

product_data = pd.read_excel(product_io, dtype=str)

none_product = []

name_list = setting.name_list
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
    text = str.upper(text)
    if text in data_country.keys():
        return data_country[text]
    else:
        return text


# PR1206-Ebony
def get_delivery(sku, country):  # 物流方式
    try:
        if product_data[product_data.SKU == sku]['is_GLS'].values[0]:
            country_list = product_data[product_data.SKU == sku]['国家'].values[0]
            if 'GLOBAL' in country_list:
                return 'GLS_BIZ_PCL'
            if country in country_list:
                return 'GLS_BIZ_PCL'
        product_size = product_data[product_data.SKU == sku]['围长'].values[0]  # 对应SKU的围长
        if country == 'DE' and product_size <= 360:
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


def get_company(consignee_name, old_company):
    split_names = re.split(r'[,]', consignee_name)
    if old_company:
        champion = old_company
    else:
        champion = ''
        for names in split_names:
            get_split_name = names.split(' ')
            for name in reversed(get_split_name):
                if name in champion_name:
                    return names
    return champion


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
    print(doorplate_number, street)
    rule = '(.*)' + doorplate_number + '[,]{0,1}$'
    re_street = re.findall(rule, doorplate_number)
    if re_street:
        return re_street[0]
    return street


def get_ez_street(street):
    ez_street = setting.ez_street
    for word in list(ez_street.keys()):
        if word in street:
            street = street.replace(word, ez_street[word])
    return street
