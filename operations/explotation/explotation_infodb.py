# -*- coding: utf-8 -*-
"""formmated_infodb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yChcZP2-ou9Oo4C9GUHvLjwWOFBlvG7K
"""
import duckdb
import itertools
import pandas as pd
import os

""" 

from google.colab import drive
drive.mount('/content/drive') """

"""### READ DATABASE"""

""" con = duckdb.connect(database='/content/drive/MyDrive/projecteADSDB/formatted/formatted.duckdb', read_only=True)

tables = con.execute("SHOW TABLES").fetchall()
tables = list([t for (t,) in tables])

tables

schema = con.execute("SELECT * FROM information_schema.tables").df()
schema


tables.sort()

def get_field_sub(x): return x.split('$')[0]

mylist = sorted(tables, key=get_field_sub)
data = dict((x.split('$')[0],list(y)) for x, y in itertools.groupby(tables, get_field_sub))

data """

"""As we can see the formatted zone have different versions of the same datasource. """

""" for ds in data:
  df = con.execute(f'SELECT * FROM {data[ds][0]}').df()
  print(f'\n\n\n ======================== {ds} ========================\n\n')
  print(df.info())
 """
"""# EXECUTION OF THE PROCESS"""

def get_field_sub(x): 
   return x.split('$')[0]

def describeExplotationDB():

  dirname = os.path.dirname(__file__)
  con = duckdb.connect(database=os.path.join(dirname, 'explotation.duckdb'), read_only=True)

  tables = con.execute("SHOW TABLES").fetchall()
  tables = list([t for (t,) in tables])

  # sort by timestamp
  tables.sort() 

  mylist = sorted(tables, key=get_field_sub)
  data = dict((x.split('$')[0],list(y)) for x, y in itertools.groupby(tables, get_field_sub))

  for ds in data:
    df = con.execute(f'SELECT * FROM {data[ds][0]}').df()
    print(f'\n\n\n ======================== {ds} ========================\n\n')
    print(df.info())

  con.close()