import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from prophet import Prophet
from concurrent.futures import ProcessPoolExecutor
import matplotlib.font_manager as fm
import os
import warnings

warnings.filterwarnings("ignore", message="The behavior of DatetimeProperties.to_pydatetime is deprecated")

# 한글 폰트 설정 함수
def set_korean_font():
    fpath = os.path.join(os.getcwd(), "NanumFont/NanumGothic.ttf")
    fontprop = fm.FontProperties(fname=fpath, size=12)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    return fontprop

# 예측 함수
def fit_and_forecast(center, total_df, periods=28):
    model = Prophet()
    total_df2 = total_df.loc[total_df['center'] == center, ['date', 'use']]
    summary_df = total_df2.groupby('date')['use'].agg('mean').reset_index()
    summary_df = summary_df.rename(columns={'date': 'ds', 'use': 'y'})
    if len(summary_df) < 2:
        return center, None, summary_df  # 데이터가 2개 미만인 경우 None 반환
    model.fit(summary_df)
    future1 = model.make_future_dataframe(periods=periods)
    forecast1 = model.predict(future1)
    return center, forecast1, summary_df

def process_center(args):
    center, total_df = args
    return fit_and_forecast(center, total_df)

def dy_predict(total_df, sample_size=10, selected_centers=None):
    fontprop = set_korean_font()
    total_df['date'] = pd.to_datetime(total_df['date'], format='%Y-%m')
    types = list(total_df['center'].unique())

    if selected_centers:
        types = [t for t in types if t in selected_centers]
    elif len(types) > sample_size:
        types = types[:sample_size]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_center, [(center, total_df) for center in types]))

    num_plots = len([result for result in results if result[1] is not None])
    rows = (num_plots + 3) // 4
    fig, axs = plt.subplots(figsize=(40, rows * 10), ncols=2, nrows=rows)
    axs = axs.flatten()

    plot_idx = 0
    for i, (center, forecast1, summary_df) in enumerate(results):
        if forecast1 is None:
            continue
        model = Prophet()
        model.fit(summary_df)
        model.plot(forecast1, uncertainty=True, ax=axs[plot_idx])
        axs[plot_idx].set_title(f'서울시 {center} 평균 사용량 예측 시나리오 {28}일간', fontproperties=fontprop)
        axs[plot_idx].set_xlabel('날짜', fontproperties=fontprop)
        axs[plot_idx].set_ylabel('평균 사용량', fontproperties=fontprop)
        for tick in axs[plot_idx].get_xticklabels():
            tick.set_rotation(30)
        plot_idx += 1

    for j in range(plot_idx, len(axs)):
        fig.delaxes(axs[j])

    fig.tight_layout()
    st.pyplot(fig)

def showPred(total_df):
    st.sidebar.header('필터링 옵션')
    sample_size = None
    centers = list(total_df['center'].unique())
    selected_centers = st.sidebar.multiselect('대여소 선택', centers, default=centers[:2])

    dy_predict(total_df, sample_size, selected_centers)

