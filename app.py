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

def sidebar_config(options, tsla_index):
    chosen_comp = st.sidebar.selectbox(label="Symbol", options=options, index=tsla_index)
    return chosen_comp

def lookup_page():
    st.title('Company Lookup')

    # data = pull_data("iwv-2002-2022-numericals.pkl")
    data = pull_data("iwv-2002-2022-objects-20230122.pkl")

    options = sorted(data.Company_Name.unique().tolist())
    tsla_index = options.index("Tesla Inc")

    # chosen_comp = st.selectbox(label="Symbol", options=options, index=tsla_index)
    chosen_comp = sidebar_config(options, tsla_index)

    firstdf = data[data.Company_Name == chosen_comp].sort_values('StartDate', ascending=False) \
        [['Sales', 'EBIT', 'EBIT_ROIC', 'OCF', 'OCF_ROIC', 'ROA', 'CurrAssets', 'Cash', 'TangibleCapital']]\
        .reset_index().reset_index(drop=True)

    seconddf = data[data.Company_Name == chosen_comp].sort_values('StartDate', ascending=False) \
        [["EBIT", "RD", "FCF", "EBIT_ROIC", "EBIT_RD_ROIC", "FCF_ROIC", "FCF_RD_ROIC", "RD_Cap", "RD_Sales"]]\
        .reset_index().reset_index(drop=True)

    thirddf = data[data.Company_Name == chosen_comp].sort_values('StartDate', ascending=False) \
        [["ShareholderYield1", "DividendYield", "DownsideBeta", "UpsideBeta", "Net_Cash", "ST_Debt", "LT_Debt"]]\
        .reset_index().reset_index(drop=True)

    fourthdf = data[data.Company_Name == chosen_comp].sort_values('StartDate', ascending=False) \
        [["EBIT_EV", "OCF_EV", "FCF_EV", "EBIT_RD_EV", "OCF_RD_EV", "FCF_RD_EV"]]\
        .reset_index().reset_index(drop=True)

    fifthdf =data[data.Company_Name == chosen_comp].sort_values('StartDate', ascending=False) \
        [['EBITGrowth-1y', 'EBITGrowth-3y', 'SalesGrowth-1y', 'SalesGrowth-3y',
          'OCFGrowth-1y', 'OCFGrowth-3y', ]]\
        .reset_index().reset_index(drop=True)

    html_styling = """
    <style>
    table {margin: 0}
    table {border-collapse: collapse}
    table {border: 2px solid white}
    table {display: block}
    table {overflow-x: auto}
    
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

    with st.beta_expander("EBIT ROIC", expanded=True):
        st.table(firstdf)
        # st.download_button(label='Download Current Result',
        #                    data=firstdf,
        #                    file_name='ebit_roic.xlsx')

    with st.beta_expander("R&D Focused", expanded=True):
        st.table(seconddf)

    with st.beta_expander("Yield, Beta, Cash & Debt", expanded=True):
        st.table(thirddf)

    with st.beta_expander("Earnings Yield Valuation", expanded=True):
        st.table(fourthdf)

    with st.beta_expander("Growth Focused", expanded=True):
        st.table(fifthdf)

def create_app_with_pages():
    # CREATE PAGES IN APP
    app = MultiApp()
    app.add_app("Simple Lookup", lookup_page, [])
    app.run(logo_path='logo.png')
    # app.run(logo_path="")

if __name__ == '__main__':
    create_app_with_pages()