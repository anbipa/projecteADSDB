# -*- coding: utf-8 -*-
"""combine_versions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l3JLhiIcrcfixC9uwJ-B9HuqiZWSpuAk
"""

import duckdb
import pandas as pd
import os
import itertools
""" 
from google.colab import drive
drive.mount('/content/drive')

con = duckdb.connect(database='/content/drive/MyDrive/projecteADSDB/formatted/formatted.duckdb', read_only=True)
print(con.execute('SELECT 1').fetchall()) """

"""We assume data integration can be done by loading the latest table of each data source based on the timestamp"""
""" 
l = con.execute("SHOW TABLES").fetchall()
out = list([t for (t,) in l])

out.sort()

def get_field_sub(x): return x.split('$')[0]

mylist = sorted(out, key=get_field_sub)
data = dict((x.split('$')[0],list(y)) for x, y in itertools.groupby(out, get_field_sub))

dsdict = {}

for ds in data:
  dsdict[ds] = pd.DataFrame()
  for dsversion in data[ds]:
    newdf = con.execute(f'SELECT * FROM {dsversion}').df()
    print(newdf.head())
    if len(data[ds])>1:
      dsdict[ds] = pd.concat([dsdict[ds],newdf], axis=0).drop_duplicates().reset_index(drop=True)
    else:
      dsdict[ds] = newdf """

"""Store data to trusted"""
""" 
con = duckdb.connect(database='/content/drive/MyDrive/projecteADSDB/trusted/trusted.duckdb', read_only=False)

for ds in dsdict:
  df = dsdict[ds]
  print(df.head())
  con.execute(f'DROP TABLE IF EXISTS {ds}')
  con.execute(f"CREATE TABLE IF NOT EXISTS {ds} AS SELECT * FROM df")

con.execute("SHOW TABLES").fetchall()

df = con.execute("SELECT * FROM Country_Level_Data").df()

df.head()

con.close() """

"""# EXECUTION OF THE PROCESS"""

def execute_combine_versions():

  dirname = os.path.dirname(__file__)
  # formatted directory
  pardir = os.path.join(dirname, "../formatted")
  # connect to formatted database
  con = duckdb.connect(database=os.path.join(pardir, 'formatted.duckdb'), read_only=True)

  l = con.execute("SHOW TABLES").fetchall()
  out = list([t for (t,) in l])

  out.sort()

  def get_field_sub(x): return x.split('$')[0]

  mylist = sorted(out, key=get_field_sub)
  data = dict((x.split('$')[0],list(y)) for x, y in itertools.groupby(out, get_field_sub))

  dsdict = {}

  for ds in data:
    dsdict[ds] = pd.DataFrame()
    for dsversion in data[ds]:
      newdf = con.execute(f'SELECT * FROM {dsversion}').df()
      if len(data[ds])>1:
        dsdict[ds] = pd.concat([dsdict[ds],newdf], axis=0).drop_duplicates().reset_index(drop=True)
      else:
        dsdict[ds] = newdf

  con = duckdb.connect(database=os.path.join(dirname, 'trusted.duckdb'), read_only=False)

  for ds in dsdict:
    df = dsdict[ds]
    con.execute(f'DROP TABLE IF EXISTS {ds}')
    con.execute(f"CREATE TABLE IF NOT EXISTS {ds} AS SELECT * FROM df")

  con.close()