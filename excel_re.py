import re
# import sys
# sys.path.append(r"langdetect")

import langdetect
import pandas as pd


def check_func(re_sql, address):
    val = re.findall(re_sql, address, re.IGNORECASE)
    if val:
        return val[0][0] or val[0][1]
    else:
        return ''


def sp_get_val(address):
    re_sql = 'Calle.*?(\d{1,}[a-z]{0,}[-/\da-z\s]{0,2})|' \
             'Calle[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
    val = check_func(re_sql, address)
    return val


def read_excel(address, delivery_country, postcode=''):
    if not pd.isnull(delivery_country):
        delivery_country = str.upper(delivery_country)

    if address[-1] != ',':
        address += ','

    if str(postcode) in address:
        address = address.replace(str(postcode), '')
    val = ''
    # if delivery_country == 'SPAIN':
    #     val = sp_get_val(address)
    # re_sql = r'strasse[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})|strasse[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
    if not val:
        re_sql = r'strasse[\s,\.]{0,}(\d{1,}[-/\da-z]{0,}\s{0,}\w{0,1})[,\s]{1,}|strasse[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'straße[\s,\.]{0,}(\d{1,}[-/\da-z]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
                 r'|straße[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'str[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
                 r'|str[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'weg[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
                 r'|weg[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'allee[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
                 r'|allee[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'stieg[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
                 r'|stieg[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'stieg[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
                 r'|stieg[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'rwall[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}){0,}\,|rwall[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'platz[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})|platz[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'(\d{1,}[-/\da-z\s]{0,1})[\s,\.]{0,}Im|([a-z]{1,}[-/\da-z]{0,}\d{1,})[\s,\.]{0,}Im'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'(\d{1,}[-/\da-z\s]{0,1})[\s\.]{0,}Rue|([a-z]{1,}[-/\da-z]{0,}\d{1,})[\s,\.]{0,}Rue'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Barenbleek[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})|Barenbleek[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Romani[\s,\.]{0,}(\d{1,}[-/\da-z,ºª\s]{0,}),|Romani[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Pusterla[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})|Pusterla[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Pla[\s,\.]{0,}(\d{1,}[-/\da-z,\s]{0,}),|Pla[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'gasse[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}\w{0,1})[,\s]{1,}' \
                 r'|gasse[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Pavia[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}),' \
                 r'|Pavia[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Packstation[\s,\.]{0,}(\d{1,}[-/\da-z,\s]{0,}),' \
                 r'|Packstation[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Tournay[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,})' \
                 r'|Tournay[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Meisenbühel[\s,\.]{0,}(\d{1,}[-/\da-z\s,]{0,}),' \
                 r'|Meisenbühel[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Hülsmannsfeld[\s,\.]{0,}(\d{1,}[-/\da-z\s,]{0,}),' \
                 r'|Hülsmannsfeld[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Ackern[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}),' \
                 r'|Ackern[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'busch[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}),' \
                 r'|busch[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Tunaima[\s,\.]{0,}(\d{1,}[-/\da-z\sº,]{0,}),' \
                 r'|Tunaima[\s,\.]{0,}([a-z]{1,}[-/\da-zº,]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'lerst[\s,\.]{0,}(\d{1,}[-/\da-z\sº,]{0,}),' \
                 r'|lerst[\s,\.]{0,}([a-z]{1,}[-/\da-zº,]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'M7[\s,\.]{0,}(\d{1,}[-/\da-z\sº,]{0,}),' \
                 r'|M7[\s,\.]{0,}([a-z]{1,}[-/\da-zº,]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Grasbrookpark[\s,\.]{0,}(\d{1,}[-/\da-z\sº]{0,}),' \
                 r'|Grasbrookpark[\s,\.]{0,}([a-z]{1,}[-/\da-zº,]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Friedhöfen[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,}),' \
                 r'|Friedhöfen[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'brogsgade[\s,\.]{0,}(\d{1,}[-/\da-z\s,\.]{0,}),' \
                 r'|brogsgade[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'straat[\s,\.]{0,}(\d{1,}[-/\da-z\s\.]{0,})[,]{0,}' \
                 r'|straat[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Horta[\s,\.]{0,}(\d{1,}[-/\da-z\s\.]{0,})[,]{0,}' \
                 r'|Horta[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Postfiliale[\s,\.]{0,}(\d{1,}[-/\da-z\s\.]{0,})[,]{0,}' \
                 r'|Postfiliale[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Lubelska[\s,\.]{0,}(\d{1,}[-/\da-z\s\.]{0,})[,]{0,}' \
                 r'|Lubelska[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Närkesgatan[\s,\.]{0,}(\d{1,}[-/\da-z\s\.]{0,}[,]{0,1}[-/\d]{0,})[,]{0,}' \
                 r'|Närkesgatan[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Nordufer[\s,\.]{0,}(\d{1,}[-/\da-z\s]{0,})' \
                 r'|Nordufer[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Plato[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|Plato[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Concordia[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|Concordia[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Concordia[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|Concordia[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Auderghem[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|Auderghem[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'Kiehlufer[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|Kiehlufer[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    if not val:
        re_sql = r'berg[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|berg[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)
    if not val:
        re_sql = r'Kennedydamm[\s,\.]{0,}(\d{1,}[-/\da-z]{0,})' \
                 r'|Kennedydamm[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'
        val = check_func(re_sql, address)

    try:
        if not val:
            if langdetect.detect(address) == 'fr':
                re_sql = r'(^\d{1,}[-/a-z\d]{0,})|(^[a-z]{1,}[-/\da-z]{0,}\d{1,})'
                val = check_func(re_sql, address)

    except:
        pass
    if not val:
        val = re.findall(r'^(\d{1,}[-/\da-z]{0,}\s{0,}\w{0,1})[,\s]{1,}|^(\d{1,})', address)
        if val and len(val) == 1:
            val = val[0][0] or val[0][1]
            if len(val) > 5:
                val = ''
        else:
            val = ''
    # r'straße[\s,\.]{0,}(\d{1,}[-/\da-z]{0,}\s{0,}\w{0,1})[,\s]{1,}' \
    #                  r'|straße[\s,\.]{0,}([a-z]{1,}[-/\da-z]{0,}\d{1,})'

    if not val:
        val = re.findall(r'(\d{1,}[a-z\s\d]{0,5})[,]{0,}|(\d{1,}[-]\d{1,}),', address,
                         re.IGNORECASE)
        if val and len(val) == 1:
            val = val[0][0] or val[0][1]
        else:
            val = ''

    if not val:
        val = re.findall(r'(\d{1,}[-/\da-z]{0,}\s{0,}\w{0,1})[,\s.]{1,}', address, re.IGNORECASE)
        if val:
            val = val[0]
        else:
            val = ''

    if not val:
        val = re.findall(r',[\s,\.]{0,}(\d{1,}[-/\da-z,]{0,}\s{0,}\w{0,1})[,\s]{1,}|,(\d{1,}[\sA-Z]{0,})', address)
        if val and len(val) == 1:
            val = val[0][0] or val[0][1]
        else:
            val = ''

    if not val:
        val = re.findall(r'(\d{1,}[-]\d{1,})[,]{0,}|(\d{1,}[-]\d{1,}),', address,
                         re.IGNORECASE)
        if val and len(val) == 1:
            val = val[0][0] or val[0][1]
        else:
            val = ''

    return val


if __name__ == '__main__':
    result = read_excel("General Manso 51 3 3,", '', 123123)
    print(result)
    # save_excel(result, '/Users/loctek/Desktop/德国订单地址数据111.xlsx')
