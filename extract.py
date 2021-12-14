import pandas as pd

def from_xslx_to_csv(filename, sheet, csvfilename = 'csvfile.csv'):
    data_xls = pd.read_excel(filename, sheet, dtype=str, index_col=None)
    data_xls.to_csv(csvfilename, encoding='utf-8', index=False)
    return csvfilename

def get_sheet_names(filename):
    xls = pd.ExcelFile(filename)

    return xls.sheet_names

def from_csv_to_dataframe(filename):
    print(filename)
    data = pd.read_csv (filename)   
    return pd.DataFrame(data)

if __name__=="__main__":
    dataframes = []
    sheet_names = get_sheet_names('data.xlsx')
    for sheet in sheet_names:
        csv = from_xslx_to_csv('data.xlsx', sheet,sheet+'.csv')
        dataframes.append(from_csv_to_dataframe(csv))

    