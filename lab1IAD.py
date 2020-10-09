# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 14:15:10 2020

@author: Оленка
"""

import pandas as pd
import make_graphics
from datetime import datetime
 
def string_to_num(string, num):     
    numbers = []
    for n in range(len(string)):
        numbers.append(int(str(string[n])[:num]))
    return numbers

def string_to_float(string):
    string1 = string.str.replace(',', '.')
    string2 = pd.to_numeric(string1)
    return string2

def string_to_date(str_date):   
    correct_date = []
    for i in range(len(str_date)):
        temp_date = datetime.strptime(str_date[i], '%d.%b').strftime('%d.%m.2019')
        correct_date.append(temp_date) 
    return correct_date

def string_to_time(str_time):  
    str_time = pd.to_datetime(str_time).apply(lambda x: x.strftime(r'%H:%M:%S'))
    return str_time

def parser_fun(DataFrame):
    DataFrame['day/month'] = list(string_to_date(DataFrame['day/month']))
    DataFrame['Wind Gust'] = string_to_num(list(DataFrame['Wind Gust']), -4)
    DataFrame['Pressure'] = list(string_to_float(DataFrame['Pressure']))
    DataFrame['Humidity'] = list(string_to_num(DataFrame['Humidity'], -1))
    DataFrame['Wind Speed'] = list(string_to_num(DataFrame['Wind Speed'], -4))
    DataFrame['Time'] = list(string_to_time(DataFrame['Time']))
    print(DataFrame)
    return DataFrame
    
if __name__ == '__main__':
    database = pd.read_csv('C:/Users/Оленка/.spyder-py3/DATABASE.csv',sep=';') 
    database = parser_fun(database)
#   database.set_index('day/month', inplace=True)
    make_graphics.create_graphics(database)



