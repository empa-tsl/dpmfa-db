# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:36:27 2019

@author: dew

To run this script, SQLite needs to be installed on the computer.
"""

import os
import pandas as pd
import sqlite3

# create or open database
connection = sqlite3.connect("example_data.db")
cursor = connection.cursor()


### COMPARTMENTS ##############################################################

# create a table for compartments
cursor.execute("""
               CREATE TABLE IF NOT EXISTS compartments (
               name TEXT,
               fulllabel TEXT,
               type TEXT,
               PRIMARY KEY(fulllabel)
               );""")

# import table
df = pd.read_csv('Compartments.csv', sep = ";", decimal = ",")

# append data to database   
df.to_sql('compartments', connection, if_exists='append', index = False)

### MATERIALS #################################################################

# create a table for materials
cursor.execute("""
               CREATE TABLE IF NOT EXISTS materials (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT
               );""")

# import table
df = pd.read_csv('Materials.csv', sep = ";", decimal = ",")

# append data to database   
df.to_sql('materials', connection, if_exists='append', index = False)

### TRANSFER COEFFICIENTS #####################################################

# create a table for transfer coefficients
cursor.execute("""
               CREATE TABLE IF NOT EXISTS transfercoefficients (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               comp1 INTEGER NOT NULL,
               comp2 INTEGER NOT NULL,
               year INTEGER,
               mat INTEGER NOT NULL,
               value DOUBLE,
               priority INTEGER NOT NULL,
               dqisgeo INTEGER NOT NULL,
               dqistemp INTEGER NOT NULL,
               dqismat INTEGER NOT NULL,
               dqistech INTEGER NOT NULL,
               dqisrel INTEGER NOT NULL,
               source TEXT,
               FOREIGN KEY(comp1) REFERENCES compartments(fulllabel),
               FOREIGN KEY(comp2) REFERENCES compartments(fulllabel),
               FOREIGN KEY(mat) REFERENCES materials(name)
               );""")

# explore directory for files
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        
        # test if "TC" is in file name, if not, skip
        if not "TC" in name:
            continue
        
        # else import table
        df = pd.read_csv(name, sep = ";", decimal = ",")
       
        # append data to database   
        df.to_sql('transfercoefficients', connection, if_exists='append', index = False)


### INPUT #####################################################################

# create a table for input
cursor.execute("""
               CREATE TABLE IF NOT EXISTS input (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               comp TEXT,
               year INTEGER,
               mat TEXT,
               value DOUBLE,
               dqisgeo INTEGER NOT NULL,
               dqistemp INTEGER NOT NULL,
               dqismat INTEGER NOT NULL,
               dqistech INTEGER NOT NULL,
               dqisrel INTEGER NOT NULL,
               source TEXT,
               FOREIGN KEY(comp) REFERENCES compartments(fulllabel),
               FOREIGN KEY(mat) REFERENCES materials(id)
               );""")


# explore directory for files
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        
        # test if "Input" is in file name, if not, skip
        if not "Input" in name:
            continue
        
        # else import table
        df = pd.read_csv(name, sep = ";", decimal = ",")
       
        # append data to database   
        df.to_sql('input', connection, if_exists='append', index = False)


### LIFETIMES #################################################################

# create a table for lifetimes
cursor.execute("""
               CREATE TABLE IF NOT EXISTS lifetimes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               comp TEXT,
               year INTEGER,
               value DOUBLE,
               FOREIGN KEY(comp) REFERENCES compartments(fulllabel)
               );""")

# import table
df = pd.read_csv('Lifetimes.csv', sep = ";", decimal = ",")

# append data to database   
df.to_sql('lifetimes', connection, if_exists='append', index = False)


# commit changes
connection.commit()

# close connection
connection.close()
