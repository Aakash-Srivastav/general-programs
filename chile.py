"""
This code is for manipulating data and table.
Used for already inserted data.
Have both Import and Export Code.
"""

import pyodbc
import pandas as pd

from conn import *

imp_table = input('enter import table name.. : ')
exp_table = input('enter export table name.. : ')
database_name = input('enter database name.. : ')

def chile_import():

  database_imp,conn_imp,cursor_imp = connection(database=database_name)

  imp_query = []

  imp_query1 = f'''
            ALTER Table {database_imp}..{imp_table} 
            ADD IMP_DATE date
            '''
  imp_query2 = f'''
            UPDATE {database_imp}..{imp_table} SET IMP_DATE = CONCAT(YEAR,'-',MONTH,'-',DAY)
            '''
  imp_query3 = f'''
            ALTER TABLE {database_imp}..{imp_table}
            ALTER COLUMN YEAR date
            '''
  imp_query4 = f'''
            UPDATE {database_imp}..{imp_table} SET YEAR = IMP_DATE
            '''
  imp_query5 = f'''
            ALTER TABLE {database_imp}..{imp_table}
            DROP COLUMN DAY,MONTH,IMP_DATE
            '''
  imp_query6 = f'''
            ALTER TABLE {database_imp}..{imp_table}
            ADD HS_CODE_2 nvarchar(4) , HS_CODE_4 nvarchar(4) , COUNTRY_ISO_CODE_2 nvarchar(4)
            '''
  imp_query7 = f'''
            UPDATE {database_imp}..{imp_table} SET HS_CODE_2 = LEFT([HS CODE],2)
            UPDATE {database_imp}..{imp_table} SET HS_CODE_4 = LEFT([HS CODE],4)
            '''
  imp_query8 = f'''
              CREATE TABLE {database_imp}..{imp_table}_new(
              [IMP_DATE] [date] NULL,
              [CUSTOM] [nvarchar](15) NULL,
              [IMPORT_ID] [nvarchar](10) NULL,
              [IMPORTER_ID] [nvarchar](10) NULL,
              [IMPORTER_ID_CHECK_DIGIT] [nvarchar](1) NULL,
              [IMPORTER_NAME] [nvarchar](80) NULL,
              [HS_CODE] [nvarchar](8) NULL,
              [HS_CODE_DESCRIPTION] [nvarchar](255) NULL,
              [PRODUCT_DESCRIPTION] [nvarchar](255) NULL,
              [BRAND] [nvarchar](200) NULL,
              [VARIETY] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_1] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_2] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_3] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_4] [nvarchar](200) NULL,
              [ORIGIN_COUNTRY] [nvarchar](50) NULL,
              [PURCHASE_COUNTRY] [nvarchar](50) NULL,
              [TRANSPORT_TYPE] [nvarchar](35) NULL,
              [TYPE_OF_PAYMENT] [nvarchar](50) NULL,
              [ORIGIN_PORT] [nvarchar](40) NULL,
              [LANDING_PORT] [nvarchar](30) NULL,
              [TRANSPORT_COMPANY] [nvarchar](40) NULL,
              [LOAD_TYPE] [nvarchar](15) NULL,
              [PACKAGE_TYPE] [nvarchar](50) NULL,
              [GROSS_WEIGHT] [float] NULL,
              [INCOTERM] [nvarchar](20) NULL,
              [TAX_PERCENTAGE] [nvarchar](10) NULL,
              [QUANTITY] [float] NULL,
              [UNIT] [nvarchar](30) NULL,
              [USD_FOB] [float] NULL,
              [USD_FREIGHT] [float] NULL,
              [USD_INSURANCE] [float] NULL,
              [USD_CIF] [float] NULL,
              [USD_CIF_PER_UNIT] [float] NULL,
              [USD_FOB_PER_UNIT] [float] NULL,
              [TRANSPORT_COMPANY_COUNTRY] [nvarchar](50) NULL,
              [USD_TAX] [float] NULL,
              [PACKAGES_QUANTITY] [nvarchar](10) NULL,
              [ECONOMIC_ZONE] [nvarchar](10) NULL,
              [IMPORTER_ECONOMIC_KEY] [nvarchar](10) NULL,
              [MANIFEST_NUMBER] [nvarchar](20) NULL,
              [MANIFEST_DATE] [nvarchar](10) NULL,
              [TRANSPORT_DOCUMENT_NUMBER] [nvarchar](35) NULL,
              [TRANSPORT_DOCUMENT_DATE] [nvarchar](10) NULL,
              [HS_CODE_2] [nvarchar](4) NULL,
              [HS_CODE_4] [nvarchar](4) NULL,
              [COUNTRY_ISO_CODE_2] [nvarchar](4) NULL)

            '''
  imp_query9 = f'''
            insert into {database_imp}..{imp_table}_new
            select * from {database_imp}..{imp_table}
            '''
  imp_query10 = f'''
                update {database_imp}..{imp_table}_new set GROSS_WEIGHT = 0 where GROSS_WEIGHT is null
                update {database_imp}..{imp_table}_new set QUANTITY = 0 where QUANTITY is null
                update {database_imp}..{imp_table}_new set USD_FOB = 0 where USD_FOB is null
                update {database_imp}..{imp_table}_new set USD_FREIGHT = 0 where USD_FREIGHT is null
                update {database_imp}..{imp_table}_new set USD_INSURANCE = 0 where USD_INSURANCE is null
                update {database_imp}..{imp_table}_new set USD_CIF = 0 where USD_CIF is null
                update {database_imp}..{imp_table}_new set USD_CIF_PER_UNIT = 0 where USD_CIF_PER_UNIT is null
                update {database_imp}..{imp_table}_new set USD_FOB_PER_UNIT = 0 where USD_FOB_PER_UNIT is null
                update {database_imp}..{imp_table}_new set USD_TAX = 0 where USD_TAX is null
                 '''

  for i in range(1,11):
    imp_query.append(locals()[f'imp_query{i}'])

  for query in imp_query:
    cursor_imp.execute(query)

  conn_imp.commit()
  conn_imp.close()

def chile_export():

  database_exp,conn_exp,cursor_exp = connection(database=database_name)

  exp_query = []

  exp_query1 = f'''
            ALTER Table {database_exp}..{exp_table} 
            ADD EXP_DATE date
            '''
  exp_query2 = f'''
            UPDATE {database_exp}..{exp_table} SET EXP_DATE = CONCAT(YEAR,'-',MONTH,'-',DAY)
            '''
  exp_query3 = f'''
            ALTER TABLE {database_exp}..{exp_table}
            ALTER COLUMN YEAR date
            '''
  exp_query4 = f'''
            UPDATE {database_exp}..{exp_table} SET YEAR = EXP_DATE
            '''
  exp_query5 = f'''
            ALTER TABLE {database_exp}..{exp_table}
            DROP COLUMN DAY,MONTH,EXP_DATE
            '''
  exp_query6 = f'''
            ALTER TABLE {database_exp}..{exp_table}
            ADD HS_CODE_2 nvarchar(4) , HS_CODE_4 nvarchar(4) , COUNTRY_ISO_CODE_2 nvarchar(4)
            '''
  exp_query7 = f'''
            UPDATE {database_exp}..{exp_table} SET HS_CODE_2 = LEFT([HS CODE],2)
            UPDATE {database_exp}..{exp_table} SET HS_CODE_4 = LEFT([HS CODE],4)
            '''
  exp_query8 = f'''
              CREATE TABLE {database_exp}..{exp_table}_new(
              [EXP_DATE] [date] NULL,
              [EXPORT_ID] [nvarchar](10) NULL,
              [CUSTOM] [nvarchar](15) NULL,
              [EXPORTER_ID] [nvarchar](10) NULL,
              [EXPORTER_ID_CHECK_DIGIT] [nvarchar](4) NULL,
              [EXPORTER_NAME] [nvarchar](50) NULL,
              [HS_CODE] [nvarchar](8) NULL,
              [HS_CODE_DESCRIPTION] [nvarchar](255) NULL,
              [PRODUCT_DESCRIPTION] [nvarchar](255) NULL,
              [VARIETY] [nvarchar](255) NULL,
              [BRAND] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_1] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_2] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_3] [nvarchar](200) NULL,
              [PRODUCT_DESCRIPTION_4] [nvarchar](200) NULL,
              [DESTINATION_COUNTRY] [nvarchar](50) NULL,
              [TRANSPORT_TYPE] [nvarchar](35) NULL,
              [TRANSPORT_COMPANY] [nvarchar](60) NULL,
              [SHIP_NAME] [nvarchar](30) NULL,
              [LOAD_TYPE] [nvarchar](15) NULL,
              [ORIGIN_PORT] [nvarchar](40) NULL,
              [LANDING_PORT] [nvarchar](40) NULL,
              [GROSS_WEIGHT] [float] NULL,
              [QUANTITY] [float] NULL,
              [UNIT] [nvarchar](30) NULL,
              [USD_FOB] [float] NULL,
              [USD_FREIGHT] [float] NULL,
              [USD_INSURANCE] [float] NULL,
              [USD_CIF] [float] NULL,
              [USD_FOB_UNIT] [float] NULL,
              [PACKAGE_TYPE] [nvarchar](50) NULL,
              [EXPORTER_REGION] [nvarchar](20) NULL,
              [PACKAGES_QUANTITY] [nvarchar](10) NULL,
              [PACKAGES_DESCRIPTION] [nvarchar](60) NULL,
              [TRANSPORT_COMPANY_COUNTRY] [nvarchar](50) NULL,
              [SALE_CONDITION] [nvarchar](40) NULL,
              [ECONOMIC_ZONE] [nvarchar](10) NULL,
              [EXPORTER_ECONOMIC_KEY] [nvarchar](10) NULL,
              [TRANSPORT_DOCUMENT_NUMBER] [nvarchar](35) NULL,
              [TRANSPORT_DOCUMENT_DATE] [nvarchar](10) NULL,
              [VOYAGE_NUMBER] [nvarchar](15) NULL,
              [INCOTERMS] [nvarchar](20) NULL,
              [HS_CODE_2] [nvarchar](4) NULL,
              [HS_CODE_4] [nvarchar](4) NULL,
              [COUNTRY_ISO_CODE_2] [nvarchar](4) NULL)
            '''
  
  exp_query9 = f'''
            insert into {database_exp}..{exp_table}_new
            select * from {database_exp}..{exp_table}
            '''
  exp_query10 = f'''
                update {database_exp}..{exp_table}_new set GROSS_WEIGHT = 0 where GROSS_WEIGHT is null
                update {database_exp}..{exp_table}_new set QUANTITY = 0 where QUANTITY is null
                update {database_exp}..{exp_table}_new set USD_FOB = 0 where USD_FOB is null
                update {database_exp}..{exp_table}_new set USD_FREIGHT = 0 where USD_FREIGHT is null
                update {database_exp}..{exp_table}_new set USD_INSURANCE = 0 where USD_INSURANCE is null
                update {database_exp}..{exp_table}_new set USD_CIF = 0 where USD_CIF is null
                update {database_exp}..{exp_table}_new set USD_FOB_UNIT = 0 where USD_FOB_UNIT is null
                '''

  for i in range(1,11):
    exp_query.append(locals()[f'exp_query{i}'])

  for query in exp_query:
    cursor_exp.execute(query)

  conn_exp.commit()
  conn_exp.close()


if __name__ == "__main__":
    chile_import()
    chile_export()