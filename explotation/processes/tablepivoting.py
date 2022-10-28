# -*- coding: utf-8 -*-
"""tablepivoting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t4d5fhRsAgyvp0Iy6tv0A43NK-fSYBBS
"""

# !pip install duckdb

import duckdb
import pandas as pd
import os

#
# """# EXECUTION OF THE PROCESS

# """

def execute_tablepivoting():
  
  dirname = os.path.dirname(__file__)
  
  # connect to explotation database
  con = duckdb.connect(database=os.path.join(dirname, '../storage/explotation.duckdb'), read_only=False)
  
  # load governance data
  #df_governance = pd.read_sql("SELECT * FROM Governance_Data", con)
  
  df_governance = con.execute("SELECT * FROM Governance_Data;").df()

  #drop irrelevant columns
  df_governance.drop(columns=['Country Name', 'Series Name'], inplace=True)
  df_governance.rename(columns={'1996 [YR1996]': '1996', '2000 [YR2000]': '2000', '2004 [YR2004]':'2004', '2008 [YR2008]':'2008', '2012 [YR2012]':'2012', '2016 [YR2016]':'2016', '2020 [YR2020]':'2020'}, inplace=True)


  df_governance = pd.melt(df_governance, id_vars=['Country Code', 'Series Code'], value_vars=['1996', '2000', '2004', '2008', '2012', '2016', '2020'], var_name='year', value_name='value')
  df_governance['year']=df_governance['year'].astype(int)

  #remove all indicators that are not estimate values
  df_governance.drop(df_governance[~df_governance['Series Code'].str.contains("EST", case=False)].index, inplace=True)


  counts = df_governance.groupby(['Country Code', 'year', 'Series Code'], as_index = False).count()

  # obtain indexes with more than one entry
  manycounts = counts[counts.value>1]

  # delete countries with repetitions
  for cc in set(manycounts["Country Code"].tolist()):
    df_governance = df_governance[df_governance["Country Code"] != cc]

  # pivot the table
  df_governance = df_governance.pivot(index=['Country Code', 'year'], columns= 'Series Code',values="value")

  df_governance.reset_index(inplace=True)

  df_governance.columns = df_governance.columns.str.rstrip('.EST')

  # store the Governance_Data dataframe into explotation database
  con.execute("DROP TABLE IF EXISTS Governance_Data;")
  con.execute("CREATE TABLE IF NOT EXISTS Governance_Data AS SELECT * FROM df_governance")

  #close the connection
  con.close()