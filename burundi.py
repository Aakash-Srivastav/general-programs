"""
This code is for manipulating data and table.
Used Unicode text file to insert data.
"""

import pyodbc
import pandas as pd

from conn import *

# imp_table = input('enter import table name.. : ')
table_name = input('enter table name to create table.. : ')
database_name = input('enter database name.. : ')
text_file = input('enter unicode text file path.. : ')

def burundi_import():

    database_imp,conn_imp,cursor_imp = connection(database=database_name)

    imp_query = []

    imp_query1 = f'''
                    DROP TABLE if exists {database_imp}..{table_name}
                    '''

    imp_query2 = f'''
                    CREATE TABLE {database_imp}..{table_name}(
                        DATE	date,
                        BTIN	nvarchar(max),
                        IMPORTER	nvarchar(max),
                        SUPPLIER	nvarchar(max),
                        ORIG	nvarchar(max),
                        DEST	nvarchar(max),
                        CHAP	nvarchar(max),
                        [4_DIGITS]	nvarchar(max),
                        HEADING	nvarchar(max),
                        HS_CODE	nvarchar(max),
                        [11_DIGITS]	nvarchar(max),
                        MARK	nvarchar(max),
                        [DESCRIPTION_OF_GOODS]	nvarchar(max),
                        QUANTITY	nvarchar(max),
                        [STAT_UNIT]	nvarchar(max),
                        [NET_WEIGHT]	nvarchar(max),
                        [GROSS_WEIGHT]	nvarchar(max),
                        CIF	nvarchar(max),
                        NPER_OF_PACKAGE	nvarchar(max),
                        FOB	nvarchar(max),
                        FREIGHT	nvarchar(max),
                        INSURANCE	nvarchar(max),
                        OTHER_COSTS	nvarchar(max),
                        TARIFF_RATE	nvarchar(max),
                        IMPORTS_DUTY	nvarchar(max),
                        EXCISE_DITY	nvarchar(max),
                        VAT	nvarchar(max),
                        WHT	nvarchar(max),
                        QUALITY_INSPECTION_FEES	nvarchar(max),
                        PV	nvarchar(max),
                        IDL	nvarchar(max),
                        MVF	nvarchar(max),
                        AUO	nvarchar(max),
                        [TOTAL_DUTY_&_TAXES]	nvarchar(max)
                        )
                    '''
    imp_query3 = f'''
                    BULK INSERt {database_imp}..{table_name} FROM '{text_file}'
                    WITH(
                    DATAFILETYPE = 'widechar',
                    FIRSTROW = 2,
                    FIELDTERMINATOR = '\t',
                    ROWTERMINATOR = '\n',
                    TABLOCK
                    )
                    '''
    imp_query4 = f'''
                    SELECT distinct(LEN([11_DIGITS])) FROM {database_imp}..{table_name}
                    '''

    for i in range(1,5):
        imp_query.append(locals()[f'imp_query{i}'])

    for query in imp_query:
        cursor_imp.execute(query)
    
    conn_imp.commit()

    sql_query = pd.read_sql_query(imp_query4,conn_imp)

    conn_imp.close()    

#len(sql_query.values.tolist())

if __name__ == "__main__":
    burundi_import()
