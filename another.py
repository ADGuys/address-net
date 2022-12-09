import copy
import pandas as pd
import os
import glob

total_path = glob.glob(os.path.join('*.xls*'))
io = total_path[0]
data = pd.read_excel(io, dtype=str)
data = data.fillna('')
print(data)
data_list = data.to_dict('records')
new_list = []
for item in data_list:
    print(item)
    if ',' in item['Unnamed: 32']:
        item_arr = item['Unnamed: 32'].split(',')
        for item_2 in item_arr:
            new_a = item
            new_a['Unnamed: 32'] = item_2
            item_3 = copy.deepcopy(new_a)
            new_list.append(item_3)
    else:
        new_list.append(item)
df_data = pd.DataFrame(new_list)
df_data.to_excel('out.xls', index=False)
