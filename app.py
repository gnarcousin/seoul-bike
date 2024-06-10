import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from utils import load_data
from home import run_home
from eda import run_eda_home
from predict import showPred

def main():
    total_df = load_data()

    with st.sidebar:
        selected = option_menu('대시보드 메뉴', ['홈', '탐색적 자료분석', '따릉이 예측'],
                                    icons=['house', 'file-bar_graph', 'graph-up-arrow'], menu_icon = 'cast', default_index = 0)
    if selected == '홈':
        run_home(total_df)
    elif selected == '탐색적 자료분석':
        run_eda_home(total_df)
    elif selected == '따릉이 예측':
        showPred(total_df)
    else:
        print('error')

if __name__ == '__main__':
    main()