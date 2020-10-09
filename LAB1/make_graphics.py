# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:09:30 2020

@author: Оленка
"""
import matplotlib.pyplot as plt

def create_graphics(database):

    print('How many graphics do you want to see?')
    num_of_graf = int(input())
    print("Available columns:\n" + "\n".join(database.columns) + "\n")
           
    for i in range(num_of_graf):
        print('\nChoose column to vizualizate:') 
        column = input()
        if column=='Temperature' or column=='Dew Point' or column=='Humidity':          
            print('\nChoose type of graphic(line/area/scatter):') 
        elif column=='Condition' or column=='Time' or column=='Wind':
            print('\nChoose type of graphic (scatter):')
        else:
            print('\nChoose type of graphic (line/scatter):')
        graphic_type = input() 
        x = 'day/month'
        database.plot(x, y=column, kind=graphic_type, label=column,color = 'red')
        
    plt.ylabel(column)    
    plt.xticks(rotation=50)
    plt.legend()
    plt.grid()
    plt.show()  

