import pyodbc
import csv
import pandas as pd

# server = input('enter server name : ')

def connection(database):

    """
    This function will connect to sql server and database
    """
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-QU4MTG2;'
                        f'Database={database};'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()

    return database,conn,cursor

if __name__ == "__main__":
    connection()