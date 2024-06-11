import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
from pingouin import ttest
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm

def twoMeans(total_df, dys_nm):
    
    st.markdown(f'### 서울시 "{dys_nm}" 2, 3월 따릉이 대여량 차이 검증')
    
    total_df['month'] = total_df['date'].dt.month

    dd_df = total_df[(total_df['center'] == dys_nm) & (total_df['month'].isin([2,3]))]
    feb_df = dd_df[dd_df['month'] == 2]
    mar_df = dd_df[dd_df['month'] == 3]

    st.markdown(f'2월 따릉이 대여량(회) : {round(feb_df["use"].mean(),3)}')
    st.markdown(f'3월 따릉이 대여량(회) : {round(mar_df["use"].mean(),3)}')

    dy_result = ttest(feb_df['use'], mar_df['use'], paired=False)

    st.dataframe(dy_result, use_container_width=True)

    if dy_result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05보다 크므로 평균 대여량 차이는 **없다.**')
    else:
        st.markdown('p-val 값이 0.05보다 작으므로 평균 대여량 차이는 **있다.**')

def corrRelation(total_df, dys_nm):
    fpath = os.path.join(os.getcwd(), "NanumFont/NanumGothicBold.ttf")
    fontprop = fm.FontProperties(fname=fpath, size=12)
    plt.rc('font', family = 'NanumGothic')

    st.markdown(f'### 서울시 "{dys_nm}" 2, 3월 따릉이 대여량 상관 분석')

    total_df['month'] = total_df['date'].dt.month
    total_df['day'] = total_df['date'].dt.day
    ddy_df = total_df[(total_df['center'] == dys_nm) & (total_df['month'].isin([2,3]))]
    ddy_feb_df = ddy_df[ddy_df['month'] == 2]
    ddy_mar_df = ddy_df[ddy_df['month'] == 3]

    st.markdown(f'2월 따릉이 평균 대여량(회) : {ddy_feb_df["use"].mean()}')
    st.markdown(f'3월 따릉이 평균 대여량(회) : {ddy_mar_df["use"].mean()}')

    ddy_result = ttest(ddy_feb_df['use'], ddy_mar_df['use'], paired=False)

    st.dataframe(ddy_result, use_container_width=True)

    if ddy_result['p-val'].values[0] > 0.05:
        st.markdown('p-val 값이 0.05보다 크므로 평균 대여량 차이는 없다.')
    else:
        st.markdown('p-val 값이 0.05보다 작으므로 평균 대여량 차이는 있다.')

    corr_df = ddy_df[['date', 'use', 'center', 'month']].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='date', y='use', data=corr_df, ax = ax)
    sns.scatterplot(x='date', y='use', data=corr_df, ax = ax, color='black', s=18)
    st.pyplot(fig)

def ShowStat(total_df) :

    total_df['date'] = pd.to_datetime(total_df['date'].astype(str),format='%Y-%m')
    
    analisys_nm = st.sidebar.selectbox('분석메뉴', ['두 집단 간의 차이 검정', '상관 분석'])
    dys_nm = st.sidebar.selectbox('대여소명', total_df['center'].unique())
    
    if analisys_nm == '두 집단 간의 차이 검정' :
        twoMeans(total_df, dys_nm)
    elif analisys_nm == '상관 분석' :
        corrRelation(total_df, dys_nm)
    else :
        st.warning('Error')
