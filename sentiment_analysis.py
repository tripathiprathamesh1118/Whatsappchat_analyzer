from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from remove_stopwords import remove_stopwords 
import streamlit as st
import pandas as pd
from collections import Counter
import nltk
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def perform_sentiment_analysis(message,df ):

    filtered_data = remove_stopwords(message)

    stop_words = filtered_data.split()
    word_counter = Counter(stop_words)

    sentiment = SentimentIntensityAnalyzer()
    sentiment_scores = sentiment.polarity_scores(filtered_data)

    x, y, z = sentiment_scores['pos'], sentiment_scores['neg'], sentiment_scores['neu']
    overall_sentiment = "Positive" if x > y and x > z else "Negative" if y > x and y > z else "Neutral"


    df = pd.DataFrame({"stop_words": stop_words})
    custom_style = ' font-weight: bold; font-size: 40px; text-decoration: underline;'
    st.write(f"<span style='{custom_style}'>Stopword Sentiment Analysis</span>", unsafe_allow_html=True)
    st.write("Top Stop Words and Sentiment Analysis")
    
    sentiment = SentimentIntensityAnalyzer()
    df["positive"] = [sentiment.polarity_scores(i)["pos"] for i in df["stop_words"]]
    df["negative"] = [sentiment.polarity_scores(i)["neg"] for i in df["stop_words"]]
    df["neutral"] = [sentiment.polarity_scores(i)["neu"] for i in df["stop_words"]]

    st.write(df.head(100000))

    return {
        "filtered_text": filtered_data,
        "top_100_words": word_counter.most_common(100),
        "sentiment_scores": sentiment_scores,
        "overall_sentiment": overall_sentiment
    }



