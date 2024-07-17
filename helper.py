from urlextract import URLExtract
import streamlit as st
import numpy as np
import pandas as pd
import re
import plotly.express as px
extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]

    words_count = []
    for message in df['message']:
        words_count.extend(message.split())

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    result_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'user', 'user': 'user'})
    st.markdown("<p style='text-align: left; font-size: 32px; font-weight: bold; '>Most active user</p>", unsafe_allow_html=True)
    st.dataframe(result_df)

    fig = px.bar(result_df, x='user', y='count', title='Bar Chart', labels={'user': 'User', 'user': 'Percentage'})
    st.plotly_chart(fig)

    fig = px.pie(result_df, names='user', values='count', title='Pie Chart')
    st.plotly_chart(fig)

    fig = px.line(result_df, x='count', y='user', title='Line Graph')
    st.plotly_chart(fig)

    return num_messages,  len(words_count), len(links),  result_df



