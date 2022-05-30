import os
import datetime

import pandas as pd
import glob

total_path = glob.glob(os.path.join('*.csv'))
# print(total_path)
now = datetime.datetime.now().strftime('%Y-%m-%d')
print(now)
# data_csv = pd.read_csv(total_path[0])
# #
# data_csv.to_excel('导出订单' + str(now) + '.xlsx', sheet_name='data', engine='xlsxwriter')
