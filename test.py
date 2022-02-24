import re
import pandas as pd


def get_ez_street(street, zip_code, consignee_company, city, doorplate):  # except street
    street = clear_comma(street)
    ez_street = {
        'TRASSE': 'tr.',
        'traße': 'tr',
        'VENUE': 've',
        'ÂTIMENT': 'ât',
        'PPARTEMENT': 'pt'
    }
    for word in list(ez_street.keys()):
        capital_words = re.findall(word, street, flags=re.IGNORECASE)
        if capital_words:
            street = street.replace(capital_words[0], ez_street[word])
    zip_code_word = ''
    consignee_company_word = ''
    city_word = ''
    doorplate_word = ''
    if not pd.isnull(zip_code):
        zip_code_word = re.findall(zip_code, street, flags=re.IGNORECASE)
        consignee_company_word = re.findall(consignee_company, street, flags=re.IGNORECASE)  # 公司
        if city != 'Hoheging':
            city_word = re.findall(city, street, flags=re.IGNORECASE)  # city
        doorplate_word = re.findall(doorplate, street, flags=re.IGNORECASE)  # doorplate
    if zip_code_word:
        street = street.replace(zip_code_word[0], '')
    if consignee_company_word:
        street = street.replace(consignee_company_word[0], '')
    if city_word:
        street = street.replace(city_word[0] + ' ', '')
    if doorplate_word:
        try:
            doorplate_re = doorplate_word[0]
            if '-' in doorplate_word[0]:
                doorplate_re = doorplate_word[0].replace('-', '\-')

            re_sql = ',(.*)' + doorplate_re + ','
            val = re.findall(re_sql, street)
            # print(val)
            if not val:
                val = ['']
            if len(val[0]) < 3:
                val = ['']
            if not val[0]:
                re_sql = '(.*)' + doorplate_re
                val = re.findall(re_sql, street)

            if not val:
                val = ['']
            if len(val[0]) < 3:
                val = ['']
            if not val[0]:
                re_sql = doorplate_re + ',(.*?,)'
                val = re.findall(re_sql, street)

            if not val:
                val = ['']
            if len(val[0]) < 3:
                val = ['']
            if not val[0]:
                re_sql = doorplate_re + ',(.*?,)'
                val = re.findall(re_sql, street)

            if not val:
                val = ['']
            if len(val[0]) < 3:
                val = ['']
            if not val[0]:
                re_sql = doorplate_re + '(.*)'
                val = re.findall(re_sql, street)

            if not val:
                val = ['']
            if len(val[0]) < 3:
                val = ['']
            mark_mes = val
            mark_mes = mark_mes[0] if mark_mes else ''
        except ZeroDivisionError:
            mark_mes = street
        consignee_company += street.replace(mark_mes, '')
        street = mark_mes
    # consignee_company = consignee_company.replace(doorplate, '')
    street = clear_comma(street)
    consignee_company = clear_comma(consignee_company)
    if consignee_company == ',':
        consignee_company = ''

    if pd.isnull(consignee_company):
        consignee_company = ''
    if len(street) > 385:
        return '||||||||||||||||||||||||||||||', consignee_company
    return street, consignee_company


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


street, consignee_company = get_ez_street(
    street='Eibiswald 399,', doorplate='399', consignee_company='',
    zip_code='123123',
    city='Hoheging')
print(street)
print(consignee_company)
