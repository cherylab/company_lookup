import pandas as pd
import requests
import json
from pandas.io.json import json_normalize
from functools import reduce
from datetime import datetime, timedelta
import openpyxl
import time
from time import mktime
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *
from plotly.graph_objs.scatter.marker import Line
from plotly.subplots import make_subplots
import xlrd
import openpyxl
import numpy as np
import re
from bs4 import BeautifulSoup
import math
import plotly.io as pio
import plot_settings
from multiapp import MultiApp
import streamlit as st
from IPython.display import display, HTML, Latex, TextDisplayObject

st.set_page_config(layout='wide')

# # dictionary of companys and google drive links
# GOOGLE_DRIVE_URL_DICT = {
#     'SPY':'https://drive.google.com/file/d/1u3q9tkmcZIKmulbz0k0k3qcDHcQnuKqt/view?usp=sharing',
#     'QQQ':'https://drive.google.com/file/d/16GAn0hYJ_zm4WSTmWSp8Q83COHVEVSd1/view?usp=sharing'
# }
#
# # function to get file from google drive
# @st.cache
# def pull_google_drive(url):
#     file_id = url.split('/')[-2]
#     dwn_url = "https://drive.google.com/uc?id=" + file_id
#     tmp = pd.read_csv(dwn_url)
#     # tmp = pd.read_excel(dwn_url)
#     return tmp

# function to reformat raw df - only for 1 ticker at a time
# @st.cache
# def reformat_dfs(d, chosen_tick):
#     format_dict = {'MarketCap': '{:,.0f}', 'Net_Cash': '{:,.0f}', 'R_D': '{:,.0f}',
#                    'FCF_ROIC': '{:,.1%}', 'EBIT_ROIC': '{:,.1%}', 'ShareholderYield1': '{:,.1%}',
#                    'DividendYield': '{:,.1%}', 'EBIT_EV': '{:,.1%}', 'FCF_RD_ROIC': '{:,.1%}',
#                    'DownsideBeta3yr': '{:.2f}', 'Total_Return': '{:.2f}', 'RD_Cap': '{:.2f}',
#                    'EBITGrowth5year': '{:,.1%}'}
#
#     tmp = d.copy()
#     return tmp

@st.cache
def pull_data(filename):
    tmp = pd.read_pickle(filename)
    return tmp


def getTableHTML(df):
    """
    From https://stackoverflow.com/a/49687866/2007153

    Get a Jupyter like html of pandas dataframe

    """

    styles = [
        # table properties
        dict(selector=" ",
             props=[("margin", "0"),
                    ("font-family", '"Helvetica", "Arial", sans-serif'),
                    ("border-collapse", "collapse"),
                    # ("border","none"),
                    ("border", "2px solid white")
                    ]),

        # header color - optional
        #     dict(selector="thead",
        #          props=[("background-color","#cc8484")
        #                ]),

        # background shading
        dict(selector="tbody tr:nth-child(odd)",
             props=[("background-color", "#fff")]),
        dict(selector="tbody tr:nth-child(even)",
             props=[("background-color", "#F6F8F9")]),

        # cell spacing
        dict(selector="td",
             props=[("padding", ".5em"),
                    ("text-align", "right"),
                    ("font-size", '14')]),

        # header cell properties
        dict(selector="th",
             props=[("font-size", "14"),
                    ("text-align", "right")]),

        dict(selector="tbody tr:hover",
             props=[('background-color', '#d9d9d9'),
                    ('cursor', 'pointer')])

    ]
    return (df.style.set_table_styles(styles)).render()


def sidebar_config(options, tsla_index):
    chosen_tick = st.sidebar.selectbox(label="Symbol", options=options, index=tsla_index)
    return chosen_tick

def lookup_page():
    st.title('Company Lookup')

    data = pull_data("iwv-2002-2022-numericals.pkl")

    options = sorted(data.Symbol.unique().tolist())
    tsla_index = options.index("TSLA-US")

    chosen_tick = sidebar_config(options, tsla_index)

    firstdf = data[data.Symbol == chosen_tick].sort_values('StartDate', ascending=False) \
        [['Sales', 'EBIT', 'EBIT_ROIC', 'OCF', 'OCF_ROIC', 'ROA', 'CurrAssets', 'Cash', 'TangibleCapital']]\
    .reset_index().reset_index(drop=True)


    html_styling = """
    <style>
    table {margin: 0}
    table {border-collapse: collapse}
    table {border: 2px solid white}
    
    tbody tr:nth-child(odd) {background-color: #fff}
    tbody tr:nth-child(even) {background-color: #f6f8f9}
    
    td {padding: .5em}
    td {text-align: right} 
    td {font-size: 14px}
    td {font-family: Helvetica}
    
    th {text-align: right}
    th {font-family: Helvetica}
    th {font-size: 14px}
    
    thead tr th:first-child {display:none}
    tbody th {display:none}
    
    tbody tr:hover {background-color: #d9d9d9}
    tbody tr:hover {cursor: "pointer"}

    </style>
    """

    st.markdown(html_styling, unsafe_allow_html=True)

    st.table(firstdf)


    # st.write(HTML(getTableHTML(firstdf)))

def create_app_with_pages():
    # CREATE PAGES IN APP
    app = MultiApp()
    app.add_app("Simple Lookup", lookup_page, [])
    app.run(logo_path='logo.png')

if __name__ == '__main__':
    create_app_with_pages()