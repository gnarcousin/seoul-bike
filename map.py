import pandas as pd
import geopandas as gpd
import streamlit as st
from geopy.distance import great_circle
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
import numpy as np
from matplotlib import rc



def find_closest_dong(station_lat, station_lon, dongs_df):
    distances = dongs_df.apply(
        lambda row: great_circle((station_lat, station_lon), (row['latitude'], row['longitude'])).meters, axis=1
    )
    return distances.idxmin()

def mapMatplot(merge_df, seoul_gpd):
    fpath = os.path.join(os.getcwd(), "NanumFont/NanumGothic.ttf")
    fontprop = fm.FontProperties(fname=fpath, size=12)
    plt.rc('font', family = 'NanumGothic')

    fig, ax = plt.subplots(figsize=(15, 10))
    
    seoul_gpd.boundary.plot(ax=ax, linewidth=1, edgecolor='black')

    norm = plt.Normalize(merge_df['mean'].min(), merge_df['mean'].max())
    cmap = plt.cm.viridis
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    sc = ax.scatter(merge_df['longitude_x'], merge_df['latitude_x'], c=merge_df['mean'], cmap=cmap, norm=norm, s=40, edgecolor='black')

    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('평균 사용량')

    ax.set_title('서울시 따릉이 대여소 사용량과 동별 지도', fontsize=16)
    ax.set_axis_off()

    st.pyplot(fig)


def showMap(total_df):
    seoul_gpd = gpd.read_file('seoul_emd.geojson.gpkg')
    seoul_gpd = seoul_gpd.set_crs(epsg ='5178', allow_override = True).to_crs(epsg = '4326')

    seoul_gpd['center_point'] = seoul_gpd['geometry'].centroid
    seoul_gpd['longitude'] = seoul_gpd['center_point'].map(lambda x: x.x)
    seoul_gpd['latitude'] = seoul_gpd['center_point'].map(lambda x: x.y)

    total_df['date'] = pd.to_datetime(total_df['date'].astype(str), format='%Y-%m')

    seoul2 = pd.read_csv('bycycle_loca.csv')

    total_df['month'] = total_df['date'].dt.month
    seoul = total_df[total_df['month'].isin([2, 3])]
    seoul = pd.concat([seoul, seoul2['latitude'], seoul2['longitude']],axis=1)

    summary_df = seoul.groupby(['latitude', 'longitude', 'date'])['use'].agg(['mean']).reset_index()

    closest_dongs = summary_df.apply(
        lambda row: find_closest_dong(row['latitude'], row['longitude'], seoul_gpd), axis=1
    )
    
    summary_df['closest_dong'] = seoul_gpd.loc[closest_dongs, 'EMD_KOR_NM'].values
    
    merge_df = pd.merge(summary_df, seoul_gpd, left_on=['closest_dong'], right_on=['EMD_KOR_NM'], how='right')
    merge_df = merge_df.sort_values('mean', ascending=False)

    seoul_gpd['latitude'] = seoul_gpd['latitude'].astype(float)
    seoul_gpd['longitude'] = seoul_gpd['longitude'].astype(float)

    st.markdown("- 일부 데이터만 확인")
    st.write(merge_df[['EMD_KOR_NM', 'mean']].head(3))
    st.markdown("<hr>", unsafe_allow_html = True)
    mapMatplot(merge_df, seoul_gpd)