#!/usr/bin/env python3

print("content-type:text/html; charset=uft-8\n")

#pip install folium

import folium
from folium.plugins import MarkerCluster, MiniMap
import pandas as pd
import numpy as np

my_info_df = pd.read_csv('비급여_도수치료_서울_강남구.csv')

data_for_draw = my_info_df.loc[:, ['병원명', '명칭', '최저비용', '최고비용', 'Xpos', 'Ypos']]

data_for_draw_except_nan = data_for_draw.dropna()

data_for_draw_except_nan['최고비용_str'] = data_for_draw_except_nan['최고비용'].str.replace(',', '')
data_for_draw_except_nan['최저비용_str'] = data_for_draw_except_nan['최저비용'].str.replace(',', '')

data_for_draw_except_nan['최고비용_int'] = data_for_draw_except_nan['최고비용_str'].astype(int)
data_for_draw_except_nan['최저비용_int'] = data_for_draw_except_nan['최저비용_str'].astype(int)

type(data_for_draw_except_nan['최저비용_int'][0])

## from tqdm import tqdm
from folium import Marker
from folium.features import CustomIcon
import branca

m = folium.Map(location=[37.5073847256628, 127.0404109009053], tiles='cartodbpositron', zoom_start = 15)
mc = MarkerCluster()

hospital_name = list(data_for_draw_except_nan['병원명'])
lat = list(data_for_draw_except_nan['Ypos'])
lon = list(data_for_draw_except_nan['Xpos'])

def fancy_html(row):
    i = row

    hospital_name = data_for_draw_except_nan['병원명'].iloc[i]
    lat = data_for_draw_except_nan['Ypos'].iloc[i]
    lon = data_for_draw_except_nan['Xpos'].iloc[i]
    treatment = data_for_draw_except_nan['명칭'].iloc[i]
    low_price = data_for_draw_except_nan['최저비용'].iloc[i]
    high_price = data_for_draw_except_nan['최고비용'].iloc[i]

    left_col_colour = "#ffffff"
    right_col_colour = "#ffffff"

    html = """<!DOCTYPE html>
<html>

<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<h4 style="margin-bottom:20px"; width="300px; align-items: center;">{}</h4>""".format(hospital_name) + """
    <style>
        .table_text_left{
            display:inline-block; /* default값 inline */
            margin-left:0px; /* 왼쪽 margin 10px */
            color:#2AC1A6;
            font-weight:bold; /* 글자형태 : 이태릭체 */
        }
        .table_text_right{
            display: table-cell;
            margin-left:0px; /* 왼쪽 margin 10px */
            color:black;
            background-color:#fffffff;
        }
    </style>
    <i class="fa-solid fa-house-chimney-medical"></i>
</head>
<table style="height: 70px; width: 100%;">
<tbody>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span class='table_text_left'>명칭</span></td>
<td style="background-color: """+ left_col_colour +""";"><span class='table_text_left'>최저비용</span></td>
<td style="background-color: """+ left_col_colour +""";"><span class='table_text_left'>최고비용</span></td>
</tr>
<tr>
<td class='table_text_right'>{}</td>""".format(treatment) + """
<td class='table_text_right'>{}</td>""".format(low_price + ' 원') + """
<td class='table_text_right'>{}</td>""".format(high_price + ' 원') + """
</tr>
</tbody>
</table>
</html>
"""
    return html

for i in range(0,len(data_for_draw_except_nan)):

    low_price_int = data_for_draw_except_nan['최저비용_int'].iloc[i]
    high_price_int = data_for_draw_except_nan['최고비용_int'].iloc[i]

    if low_price_int <= 50000:
        color = 'lightgreen'
    elif low_price_int > 50000 and low_price_int <= 100000:
        color = 'green'
    else:
        color = 'darkgreen'

    html = fancy_html(i)

    iframe = branca.element.IFrame(html=html,width=270,height=200)
    popup = folium.Popup(iframe,parse_html=True)

    folium.Marker([data_for_draw_except_nan['Ypos'].iloc[i], data_for_draw_except_nan['Xpos'].iloc[i]],
                  popup=popup,
                  tooltip = data_for_draw_except_nan['병원명'].iloc[i] + ' : ' + data_for_draw_except_nan['최저비용'].iloc[i] + '원' + ' ~ ' + data_for_draw_except_nan['최고비용'].iloc[i] + '원',
                  icon=folium.Icon(color=color, icon='plus', prefix='fa')
                 ).add_to(m)

m.save("Map1.html")
