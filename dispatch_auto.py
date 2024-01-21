"""
This is Task Specific Code created for a particular usecase.
"""

import pandas as pd
import numpy as np
import os
from conn import *

sheet = input('Enter the dispatch sheet path for reading the data : ')
database_name = input('enter database name.. : ')
table_name = input('enter table name.. : ')
folder_name = input('Enter the dispatch folder path : ')
query_list = []

def var ():
    global query
    query = f'''select top 10 * from {database_name}..{table_name} where'''
    return query

def hs_code_fn(number):

    global query
    var()

    if str(list(sheet['hs_code'])[number]) != 'nan':
        hs_list = str(list(sheet['hs_code'])[number]).split(',')

        for num in range(len(hs_list)):
            globals()[f"hs_{num+1}"] = f"""hs_code like '{hs_list[num]}%'"""

        hs_code_var = ''

        if len(hs_list) == 1:
            hs_code_var = globals()[f'hs_1']
        elif len(hs_list)>1:
            for num in range(len(hs_list)):
                if num == 0:
                    hs_code_var = hs_code_var + '' + globals()[f'hs_{num+1}']
                else:
                    hs_code_var = hs_code_var + ' or ' + globals()[f'hs_{num+1}']
        hs_code_var = '(' + hs_code_var + ')'

        query = query + ' ' + hs_code_var
    return query

def product_fn(number):
    global query

    hs_code_fn(number)

    if str(list(sheet['product'])[number]) != 'nan':
        product_list = list(sheet['product'])[number].split(',')

        for num in range(len(product_list)):
            globals()[f"product_{num+1}"] = f"""product_desc_en like '%{product_list[num]}%'"""

        product_list_var = ''

        if len(product_list) == 1:
            product_list_var = globals()[f'product_1']
        elif len(product_list)>1:
            for num in range(len(product_list)):
                if num == 0:
                    product_list_var = product_list_var + '' + globals()[f'product_{num+1}']
                else:
                    product_list_var = product_list_var + ' and ' + globals()[f'product_{num+1}']
        product_list_var = '(' + product_list_var + ')'

        if query[-5:] == 'where':
            query = query + ' ' + product_list_var
        else:
            query = query + ' and ' + product_list_var
    return query

def indian_port_fn(number):
    global query

    product_fn(number)
    
    if str(list(sheet['indian_port'])[number]) != 'nan':
        indian_port_list = list(sheet['indian_port'])[number].split(',')

        for num in range(len(indian_port_list)):
            globals()[f"indian_port_{num+1}"] = f"""indian_port like '%{indian_port_list[num]}%'"""

        indian_port_list_var = ''

        if len(indian_port_list) == 1:
            indian_port_list_var = globals()[f'indian_port_1']
        elif len(indian_port_list)>1:
            for num in range(len(indian_port_list)):
                if num == 0:
                    indian_port_list_var = indian_port_list_var + '' + globals()[f'indian_port_{num+1}']
                else:
                    indian_port_list_var = indian_port_list_var + ' or ' + globals()[f'indian_port_{num+1}']
        indian_port_list_var = '(' + indian_port_list_var + ')'

        if query[-5:] == 'where':
            query = query + ' ' + indian_port_list_var
        else:
            query = query + ' and ' + indian_port_list_var
    return query

def comapny_fn(number):
    global query

    indian_port_fn(number)

    if str(list(sheet['company'])[number]) != 'nan':
        company_list = list(sheet['company'])[number].split(',')

        for num in range(len(company_list)):
            globals()[f"company_{num+1}"] = f"""importer_name_en like '%{company_list[num]}%'"""

        company_list_var = ''

        if len(company_list) == 1:
            company_list_var = globals()[f'company_1']
        elif len(company_list)>1:
            for num in range(len(company_list)):
                if num == 0:
                    company_list_var = company_list_var + '' + globals()[f'company_{num+1}']
                else:
                    company_list_var = company_list_var + ' and ' + globals()[f'company_{num+1}']
        company_list_var = '(' + company_list_var + ')'

        if query[-5:] == 'where':
            query = query + ' ' + company_list_var
        else:
            query = query + ' and ' + company_list_var
    return query

def queries(sheet_name):
    global query
    database,conn_imp,cursor = connection(database=database_name)
    for elem in range(len(sheet_name)):
        comapny_fn(elem)
        query_list.append(query)
    for num in range(len(query_list)):
        df = pd.read_sql_query(query_list[num],conn_imp)
        df = df.fillna('NULL')
        if df.shape[0] != 0:
            df.to_excel(rf'''{folder_name}\{sheet['file_name'][num]}.xlsx''',index=False)


if __name__ == "__main__":
    queries(sheet_name=sheet)



