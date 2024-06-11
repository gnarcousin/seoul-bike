import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from viz import ShowViz
from statistic import ShowStat
from map import showMap

def home():
    st.markdown(
        '### Visualization 개요\n'
        '- 지역별 따릉이 대여 추세\n'
        '- 연도별 따릉이 대여 추세\n'
        '- 월별 따릉이 대여 추세\n'         
                )
    st.markdown(
        '### Statistics 개요\n'
        '- 서울시 대여소별 2, 3 월 따릉이 대여량 차이 검증\n'
        '- 서울시 대여소별 2, 3 월 따릉이 대여량의 상관분석\n'
    )
    st.markdown(
        '### Map 개요\n'
        '- 서울시 대여소 사용량과 동별 지도\n'
    )

def run_eda_home(total_df):
    st.markdown(
        '### 탐색적 자료분석 개요 \n'
        '탐색적 자료 분석 페이지입니다.'
                )

    selected = option_menu(
        None, ["Home", "Visualization", "Statistics", "Map"], 
        icons = ['house', 'bar-chart', 'file-spreadsheet', 'map'],
        menu_icon = 'cast', default_index=0, orientation='horizontal',
        styles={
            'container' : {
                'padding' : '0! important',
                'background-color' : '#808080'
                },
            'icon' : {
                'color' : 'orange',
                'font-size' : '25px'
                },
            'nav-link' : {
                    'font-size' : '15px',
                    'text-align' : 'left',
                    'margin' : '0px',
                    '--hover-color' : '#eee'
            },
            'nav-link-selected' : {
                    'background-color' : '#green'
            }
        })
    
    if selected == "Home":
        home()
    elif selected == "Visualization":
        ShowViz(total_df)
    elif selected == "Statistics":
        ShowStat(total_df)
    elif selected == "Map":
        showMap(total_df)
    else:
        st.warning('Wrong')
