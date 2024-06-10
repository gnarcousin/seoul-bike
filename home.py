import pandas as pd
import streamlit as st
from millify import prettify

def run_home(total_df):
    st.markdown(
        "## 대시보드 개요 \n"
        "본 프로젝트는 서울시 따릉이 공유 서비스 현황을 알려주는 대시보드 입니다."
        "여기에 추가하고 싶은 내용을 추가하면 됩니다."
                )
    
    total_df['date'] = pd.to_datetime(total_df['date'].astype(str),format='%Y-%m')
    total_df['month'] = total_df['date'].dt.month
    total_df['year'] = total_df['date'].dt.year

    dys_nm = st.sidebar.selectbox('대여소', total_df['center'].unique())

    dy_year = st.sidebar.selectbox('년도', [2017, 2018, 2019, 2020, 2021, 2022, 2023])

    month_dic = {'1월': 1, '2월': 2, '3월': 3, '4월': 4, '5월': 5, '6월': 6,
                 '7월': 7, '8월': 8, '9월': 9, '10월': 10, '11월': 11, '12월': 12}

    selected_month = st.sidebar.radio('확인하고 싶은 월을 선택하시오', list(month_dic.keys()))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{dys_nm} ({dy_year}년 {selected_month} 따릉이 대여량)')
    st.markdown("자치구와 월을 클릭하면 자동으로 각 대여소에서 대여한 **대여량**을 확인할 수 있습니다.")

    filtered_month = total_df[total_df['month'] == month_dic[selected_month]]
    filtered_month = filtered_month[filtered_month['year'] == dy_year]

    # 연도와 월별 대여량 합계 및 평균 대여량 계산
    total_rentals_month = filtered_month['use'].sum()
    num_centers_month = filtered_month['center'].nunique()
    average_rent_month = total_rentals_month / num_centers_month if num_centers_month > 0 else 0

    filtered_month = filtered_month[filtered_month['center'] == dys_nm]
    min_rent = filtered_month['use'].min()

    # 연도별 전체 대여량 계산
    filtered_year = total_df[total_df['year'] == dy_year]
    total_rentals_year = filtered_year['use'].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label=f'{dys_nm} 대여량(회)', value= prettify(min_rent))
    with col2:
        st.metric(label= f'{dy_year}년 {selected_month} 전체 대여량의 평균 (회)', value = prettify(average_rent_month))
    with col3:
        st.metric(label= f'{dy_year}년 전체 대여량 (회)', value = prettify(total_rentals_year))