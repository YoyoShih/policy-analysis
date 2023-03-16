from os import listdir
from pandas import DataFrame, concat
import pdfplumber

path = 'C:\\Users\\shih\\ActuaViz\\docs\\premiums\\國泰\\clean'
files = listdir(path)   # "files" is a list object

def ReadTable(table):
    factor = DataFrame(columns=[])
    factors = ['factor 1']
    data = None
    num = 1
    first = True
    for row in table:
        try:
            float(row[1].replace(',', ''))
            if first:
                factors.append('GP')
                data = DataFrame(columns=factors)
                first = False
            age = row[0]
            row = row[1:]
            for index, ele in enumerate(row):
                if is_number(ele):
                    new = DataFrame([([age] + list(factor.iloc[index]) + [float(ele.replace(',', ''))])], columns=factors)
                    data = concat([data, new], ignore_index=True)
        except:
            row = row[1:]
            if any(row):
                num += 1
                temp = None
                for index, ele in enumerate(row):
                    if ele != None:
                        temp = ele
                    else:
                        row[index] = temp
                factor[f'factor{num}'] = row
                factors.append(f'factor{num}')
    return data

def is_number(ele):
    try:
        float(ele.replace(',', ''))
        return True
    except:
        return False

for file in files:
    print(file)
    with pdfplumber.open(f'{path}\\{file}') as pdf:
        data_table = None
        for page in pdf.pages:
            for table in page.extract_tables():
                # print(table)
                data = ReadTable(table)
                data_table = concat([data_table, data], ignore_index=True)
        # print('-' * 150)
        print(data_table)