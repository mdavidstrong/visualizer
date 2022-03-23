#import os
import pandas as pd
from estimated_time import EstimatedTimes
from spa_date import SpaDate

# --------------- this was for when there were individual comp issue excel files ------------------ #
""" gets the current working directory and drills into excel_files dir
excel_files dir used to keep cwd clean from the large number of cs data from Greg """
# cwd = os.path.abspath('')
# excel_files_dir = cwd + '\excel_files'

""" gets the list of files from cwd """
# files = os.listdir(excel_files_dir)

""" this uses seperated date files from greg
creates a new dataframe and appends data for each excel file in 'files' """
# df = pd.DataFrame()
# for i in files:
#     if i.endswith('.xlsx'):
#         excel_file = pd.ExcelFile(excel_files_dir + '\\' + i)
#         sheets = excel_file.sheet_names
#         # only adds the sheet with 'Components and Issues' name
#         frame = excel_file.parse(sheet_name='Components and Issues')
#         df = df.append(frame)
# -------------------------------------------------------------------------------------------------- #

# this uses the new file from stover that has all data already together
df = pd.read_excel('Components and Issues.xlsx')

# removes the columns that aren't necessary
df = df.drop('(Do Not Modify) Case',axis=1)
df = df.drop('(Do Not Modify) Row Checksum',axis=1)
df = df.drop('(Do Not Modify) Modified On',axis=1)

# rename columns
df = df.rename(columns={"Serial Number (Inventory) (Inventory)":"Serial Number"})

# resets the index because each appended file starts over at '0'
df = df.reset_index()

# removes the extra index
df = df.drop('index',axis=1)

# create a cleaned date column
def clean_date(row):
    a = row['Created On']
    return str(a)[:10]
df['cleaned_date'] = df.apply(lambda row: clean_date(row), axis=1)

# create an estimated fix time column
mytimes = EstimatedTimes('est_fix_time.xlsx')
def est_time(row):
    comp = row['Primary Components']
    issue = row['Issue Description']
    if comp in mytimes.time_map().keys():
        if issue in mytimes.time_map()[comp].keys():
            return str(mytimes.time_map()[comp][issue])
    return 'no time data'
df['est_fix_time'] = df.apply(lambda row: est_time(row), axis=1)


myspadate = SpaDate(df)
df = myspadate.add_spa_date_column()

# writes dataframe to new aggregate file
# write code to automatically append the date??
df.to_excel('aggregate.xlsx')