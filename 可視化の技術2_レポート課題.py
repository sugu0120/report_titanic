import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium

df_crop = pd.read_csv('嗜好品生産量_2020.csv', encoding='utf-8')

st.title('世界の嗜好品生産量マップ')

items = ['全て'] + list(df_crop['Item'].unique())

select_item = st.selectbox('表示する嗜好品を選択してください', items)

value_ranges = {
    'カカオ豆': (0, 3_000_000),
    'コーヒー豆': (0, 9_000_000),
    '茶葉': (0, 15_000_000)
}

color_map = {
    'カカオ豆': 'yellow',
    'コーヒー豆': 'brown',
    '茶葉': 'green'
}

df_filtered = df_crop if select_item == '全て' else df_crop[df_crop['Item'] == select_item]

if select_item == '全て':
    item_filters = {}
    for item in df_filtered['Item'].unique():
        min_val, max_val = value_ranges[item]
        item_filters[item] = st.slider(
            f'{item} の生産量範囲',
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
            step=10_000
        )
else:
    min_val, max_val = value_ranges[select_item]
    item_filters = {
        select_item: st.slider(
            f'{select_item} の生産量範囲',
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
            step=10_000
        )
    }

m = folium.Map(location=[0, 0], tiles='cartodbdark_matter', zoom_start=2)


for item, (min_val, max_val) in item_filters.items():
    filtered_item_data = df_filtered[
        (df_filtered['Item'] == item) &
        (df_filtered['Value'] >= min_val) &
        (df_filtered['Value'] <= max_val)
    ]

    for _, row in filtered_item_data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=np.log(row['Value'] + 1),  # 生産量に基づくマーカーサイズ
            color=color_map.get(row['Item'], 'blue'),
            fill=True,
            fill_color=color_map.get(row['Item'], 'blue'),
            fill_opacity=0.7,
            popup=f"{row['Area_jp']} {row['Value']}"
        ).add_to(m)

st_folium(m, width=1000, height=600)
