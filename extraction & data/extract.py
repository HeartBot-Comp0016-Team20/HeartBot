import pandas as pd
import sqlite3


def from_xslx_to_csv(filename, sheet, csvfilename = 'csvfile.csv'):
    data_xls = pd.read_excel(filename, sheet, dtype=str, index_col=None)
    data_xls.to_csv(csvfilename, encoding='utf-8', index=False)
    return csvfilename

def get_sheet_names(filename):
    xls = pd.ExcelFile(filename)

    return xls.sheet_names

def from_csv_to_dataframe(filename):
    data = pd.read_csv (filename)   
    return pd.DataFrame(data)

def connect_dataframe_to_database(dfs, conn):
    i = 0
    for df in dfs:
        df.to_sql(name='tablename' + str(i), con = conn)
        i+=1

if __name__=="__main__":
    dataframes = []
    conn = sqlite3.connect('data.db')

    if conn is None:
        sheet_names = get_sheet_names('data.xlsx')

        for sheet in sheet_names:
            csv = from_xslx_to_csv('data.xlsx', sheet,sheet+'.csv')
            dataframes.append(from_csv_to_dataframe(csv))

    connect_dataframe_to_database(dataframes,conn)
    cursor = conn.execute("SELECT * FROM tablename0")
    for row in cursor:
        print(row[1:])
    conn.commit()
    conn.close()

    # #Create Database - One Time
    # dataframes = []
    # sheet_names = get_sheet_names('data.xlsx')

    # for sheet in sheet_names:
    #     csv = from_xslx_to_csv('data.xlsx', sheet,sheet+'.csv')
    #     dataframes.append(from_csv_to_dataframe(csv))

    