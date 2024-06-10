import pandas as pd

def load_data():
    data = pd.read_csv('bycycle2.csv')
    return data