import re
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import sentiment_analysis
import remove_stopwords

def preprocess(data):
    pattern = r'\[\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\]'
    messages = re.split(pattern, data)[1: ]
    dates = re.findall(pattern, data)
    
    def custom_date_parser(date_str):
        date_str = date_str.strip('[]')  # Remove brackets
        return pd.to_datetime(date_str, format='%d/%m/%y, %H:%M:%S')

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].apply(custom_date_parser)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    user = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]: #user name
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('group_notification')
            messages.append(entry[0])

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second

    df['message'] = df['message'].apply(remove_stopwords.remove_stopwords)

    return df 

