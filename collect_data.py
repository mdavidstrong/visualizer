import os
import pandas as pd

# gets the current working directory and drills into excel_files dir
# excel_files dir used to keep cwd clean from the large number of cs data from Greg
cwd = os.path.abspath('')
excel_files_dir = cwd + '\excel_files'
# gets the list of files from cwd
files = os.listdir(excel_files_dir)

# creates a new dataframe and appends data for each excel file in 'files'
df = pd.DataFrame()
for i in files:
    if i.endswith('.xlsx'):
        excel_file = pd.ExcelFile(excel_files_dir + '\\' + i)
        sheets = excel_file.sheet_names
        # only adds the sheet with 'Components and Issues' name
        frame = excel_file.parse(sheet_name='Components and Issues')
        df = df.append(frame)

# removes the columns that aren't necessary
df = df.drop('(Do Not Modify) Case',axis=1)
df = df.drop('(Do Not Modify) Row Checksum',axis=1)
df = df.drop('(Do Not Modify) Modified On',axis=1)

# resets the index because each appended file starts over at '0'
df = df.reset_index()

# removes the extra index
df.drop('index',axis=1)

# create a cleaned date column
def clean_date(row):
    a = row['Created On']
    return str(a)[:10]

df['cleaned_date'] = df.apply(lambda row: clean_date(row), axis=1)

# writes dataframe to new aggregate file
# write code to automatically append the date??
df.to_excel('new_aggregate_030422.xlsx')