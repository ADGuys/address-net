from dbhepler.mysqlhelper import DBPipeline

db_helper = DBPipeline()
db_helper.cursor.execute("""select * from view_address_check_bigdate""")
data = db_helper.cursor.fetchall()
fields = [field[0] for field in db_helper.cursor.description]
data_list = [dict(zip(fields, item)) for item in data]

data_new = data[
    ['name', 'receiveman', 'countryname', 'city',
     'street', 'receivezip', 'phone', 'statezone', 'email', 'company']]

data_new.columns = setting.new_columns
