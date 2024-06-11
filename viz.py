import streamlit as st
import pandas as pd
import plotly.express as px

def whereChart(total_df):
    st.markdown('## 지역별 따릉이 평균 대여 추세 \n')
    st.write(f'{dys_nm} 대여소의 전체 따릉이 평균 대여 추세')
    
    dys_nm = st.sidebar.selectbox('대여소', total_df['center'].unique())
    filtered_df = total_df[total_df['center'] == dys_nm]

    fig = px.line(
        filtered_df,
        x = 'date',
        y = 'use'
    )
    st.plotly_chart(fig)

def meanChart(total_df):
    st.markdown('## 연도별 따릉이 평균 대여 추세 \n')

    dys_nm2 = st.sidebar.selectbox('대여소', total_df['center'].unique())
    st.write(f'{dys_nm2} 대여소의 연도별 따릉이 평균 대여 추세')
    
    total_df['date'] = pd.to_datetime(total_df['date'].astype(str), format='%Y-%m')
    total_df['year'] = total_df['date'].dt.year
    
    filtered_df = total_df[total_df['center'] == dys_nm2]
    year_rental_total = filtered_df.groupby('year')['use'].sum().reset_index()

    fig2 = px.line(
        year_rental_total,
        x = 'year',
        y = 'use'
    )
    st.plotly_chart(fig2)

def monthChart(total_df):
    st.markdown('## 월별 따릉이 평균 대여 추세 \n')
    
    dys_nm3 = st.sidebar.selectbox('대여소', total_df['center'].unique())
    st.write(f'{dys_nm3} 대여소의 월별 따릉이 평균 대여 추세')
    
    total_df['date'] = pd.to_datetime(total_df['date'].astype(str), format='%Y-%m')
    total_df['month'] = total_df['date'].dt.month
    
    filtered_df = total_df[total_df['center'] == dys_nm3]
    month_rental_total = filtered_df.groupby('month')['use'].mean().reset_index()

    fig3 = px.line(
        month_rental_total,
        x = 'month',
        y = 'use'
    )
    st.plotly_chart(fig3)

def barChart(total_df):
    pass

def ShowViz(total_df):
    selected = st.sidebar.radio('차트메뉴', ['지역별 따릉이 평균 대여 추세', '연도별 따릉이 총 대여 수 추세', '월별 따릉이 평균 대여수 추세'])

    if selected == '지역별 따릉이 평균 대여 추세':
        whereChart(total_df)
    elif selected == '연도별 따릉이 총 대여 수 추세':
        meanChart(total_df)
    elif selected == '월별 따릉이 평균 대여수 추세':
        monthChart(total_df)
    else:
        st.warning('Error')
