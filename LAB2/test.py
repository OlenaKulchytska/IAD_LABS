# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab
import geopandas as gpd
import seaborn as sns
import sys
import time
import xlsxwriter
sns.set(style="darkgrid")

def read_file(file):
    df = pd.read_csv(file, sep = ',', encoding='utf8', parse_dates=[0], decimal = '.')
    return df

def parse(df):
    df['zvit_date'] = pd.to_datetime(df['zvit_date']).dt.strftime('%Y-%m-%d')
    return df

def line(database, col, region):
        x = list(database['zvit_date'])
        y = list(database[col])
        x1 = range(len(x))
        pylab.xticks(x1, x)
        plt.xticks(x1[::10], rotation = 90)
        plt.plot(x1, y, 'r', label = region)
        plt.xticks(rotation = 90)
        plt.xlabel('дата')
        plt.title('Динаміка ' + col + ' (' + region + ' область)')
        plt.legend(loc='lower right')


def line2(database, col, region, colour):
    x = list(database['zvit_date'])
    y = list(database[col])
    x1 = range(len(x))
    pylab.xticks(x1, x)
    plt.xticks(x1[::10], rotation=90)
    plt.plot(x1, y,  colour,label=region)
    plt.xticks(rotation=90)
    plt.xlabel('дата')
    plt.title('Динаміка ' + col + ' (' + region + ' область)')
    plt.legend(loc='lower right')

def area_counts(area):
    area1 = df.loc[df['registration_area'] == area]
    area_df = area1.groupby('zvit_date').aggregate(sum) 
    area_df = area_df.reset_index() 
    return area_df

# file = input('Enter path to file:\n')
print("------------Loading Date------------")
print("#")
time.sleep(2)
print("##")
time.sleep(2)
print("###")
file = 'C:/Users/Оленка/lab2IAD/covid19_by_settlement_dynamics.csv'
df = read_file(file)
parse(df)
#pd.set_option('display.max_columns', 9)
print(df)


# column = input('\nChoose: active_confirm, new_susp, new_confirm, new_death, new_recover\n')
print("\nChoose:\n 1 - active_confirm\n 2 - new_susp\n 3 - new_confirm\n 4 - new_death\n 5 - new_recover\n")
col_input = int(input())
if col_input == 1:
    column = 'active_confirm'
elif col_input == 2:
    column = 'new_susp'
elif col_input == 3:
    column = 'new_confirm'
elif col_input == 4:
    column = 'new_death'
elif col_input == 5:
    column = 'new_recover'
else:
    print("Choose from the list")
    sys.exit()

n = input('Choose the total of regions(number/all)?\n')
if n == 'all':
    areas = np.unique(df['registration_area'])
else:
    areas = input('Choose the name of region(s)?\n').split(", ")

for area in areas:
    line(area_counts(area), column, area)
    plt.show()

print("In one picture?(y/n)")
ans = str(input())
if ans == 'y':
    colour = 'r'
    for area in areas:
        if area == areas[0]:
            colour = 'r'
            line2(area_counts(area), column, area, colour)
        elif area == areas[1]:
            colour = 'b'
            line2(area_counts(area), column, area, colour)
        elif area == areas[2]:
            colour = 'g'
            line2(area_counts(area), column, area, colour)
        elif area == areas[3]:
            colour = 'y'
            line2(area_counts(area), column, area, colour)
        elif area == areas[4]:
            colour = 'k'
            line2(area_counts(area), column, area, colour)
    plt.show()
else:
    print(" ")

print(area_counts(area))
# -----------------MAP ---------------
ukraine = 'C:/Users/Оленка/lab2IAD/gadm36_UKR_shp/gadm36_UKR_1.shp'
regions = gpd.read_file(ukraine)
regions.loc[:, 'registration_area'] = [['Черкаська'], ['Чернігівська'], ['Чернівецька'], ['Крим'], ['Дніпропетровська'], ['Донецька'], ['Івано-Франківська'], ['Харківська'], ['Херсонська'], ['Хмельницька'], ['Київська'], ['м. Київ'], ['Кіровоградська'], ['Львівська'], ['Луганська'], ['Миколаївська'], ['Одеська'], ['Полтавська'], ['Рівненська'], ['Севастополь'], ['Сумська'], ['Тернопільська'], ['Закарпатська'], ['Вінницька'], ['Волинська'], ['Запорізька'], ['Житомирська']]
#print(regions)


df1 = df[['zvit_date', 'registration_area', 'registration_region', 'registration_settlement']]
df1.loc[:, column] = df[column]
#print(df1)

df2 = df1.loc[df1['zvit_date'] == '2020-10-20']
data = df2.groupby('registration_area').sum()
print("-----------Data grouped by feature------------\n")
print(data)


merged = regions.set_index('registration_area').join(data)
merged = merged.reset_index()
merged = merged.fillna(0)
merged1 = merged
# print(merged)

print("Do you want vizualizate on the pie?(y/n)")
ans=str(input())
if ans == 'y':
    names = merged['registration_area']
    plt.figure(figsize=(10, 10))
    total = merged[column]
    names = names[:]
    total = total[:]
    plt.pie(total, autopct='%.1f', labels=names)
    plt.title('Розподіленість областей (' + column + ')')
    plt.show()
else:
    print(" ")

print("Do you want vizualizate on the bar?(y/n)")
ans=str(input())
if ans == 'y':
    x = df['registration_area']
    plt.figure(figsize=(20, 20))
    plt.ylabel('Count')
    plt.xlabel('registration_area')
    plt.hist(x, density=False, bins=30, color='red')
    plt.xticks(rotation=90)
    plt.title('Розподіленість областей (' + column + ')')
    plt.show()
else:
    print(" ")

#1    print(merged)


print("Do you want vizualizate on the map?(y/n)")
ans=str(input())
if ans == 'y':
    fig, ax = plt.subplots(1, figsize=(40, 20))
    ax.axis('off')
    ax.set_title('Карта захворюваності України', fontdict={'fontsize': '20', 'fontweight' : '3'})


    vmin, vmax = 0, 30000
    sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig.colorbar(sm)
    cbar.ax.tick_params(labelsize=20)

    merged.plot(column, cmap='RdBu_r', linewidth=0.8, ax=ax, figsize=(40,20))
    plt.show()
else:
    print(" ")

print("Do you want to write to exsel?(y/n)")
ans=str(input())
if ans == 'y':
    with pd.ExcelWriter("C:/Users/Оленка/lab2IAD/Res.xlsx", sheet_name='Sheet2', engine='openpyxl',
                        mode='a') as writer:
        data.to_excel(writer)
    dataframe = pd.DataFrame()
    writer = pd.ExcelWriter('C:/Users/Оленка/lab2IAD/Res2.xlsx', engine='xlsxwriter')
    excel = input('Do you want to write your dataframe to a file?(1 or 0)\n')
    if excel == '1':
        for area in areas:
            dataframe1 = df.loc[df['registration_area'] == area]
            dataframe = dataframe1.groupby('zvit_date').aggregate(sum)
            dataframe.to_excel(writer, area)
        writer.save()
    elif excel == '0':
        print('ok')
else:
    sys.exit()
