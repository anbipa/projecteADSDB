# -*- coding: utf-8 -*-
"""profiling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jffQ6GJTlKAEqEUrjRuHtNDPJZKAtARL
"""

# !pip install duckdb
import duckdb
import os
from pandas_profiling import ProfileReport
# ! pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip


"""# EXECUTION OF THE PROCESS"""

def execute_profiling():

  dirname = os.path.dirname(__file__)

  # connect to trusted database
  con = duckdb.connect(database=os.path.join(dirname, '../../storage/trusted.duckdb'), read_only=True)

  # obtain table names
  tables = con.execute("SHOW TABLES").fetchall()
  tables = list([t for (t,) in tables])

  #profile tables
  if os.path.exists(os.path.join(dirname, 'profile_reports')) == False:
        os.mkdir(os.path.join(dirname, 'profile_reports'))

  for ds in tables:
    df = con.execute(f'SELECT * FROM {ds}').df()
    print(f'\n\nCreating report for {ds} DataSource...\n')
    profile = ProfileReport(df, title=ds, html={'style' : {'full_width':True}})
    profile.to_file(os.path.join(dirname, f'./profile_reports/{ds}_report.html'))
  # close connection
  con.close()
