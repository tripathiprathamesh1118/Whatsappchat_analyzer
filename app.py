import re
import pandas as pd
import streamlit as st
import urlextract
import preprocessor, helper, remove_stopwords
from sentiment_analysis import perform_sentiment_analysis
from remove_stopwords import remove_stopwords
import json
import requests
from streamlit_lottie import st_lottie

def homepage():
    custom_style = ' font-weight: bold; font-size: 56px;  text-decoration: underline; '
    st.write(f"<br><span style='{custom_style}'>Whatsapp Chat Analyser for Investigation</span>", unsafe_allow_html=True)

    custom_style = ' font-size: 30px; '
    st.write(f"<br><br><br><span style='{custom_style}'>Login</span>", unsafe_allow_html=True)
    user_input = st.text_input("Your Email is:", " ")
    user_input = st.text_input("Your Password is:", " ")
    if st.button("Enter"):
        with open("user_input.txt", "w") as f:
            f.write(user_input)
        st.success("Input saved!")
    if st.checkbox("Password"):
        try:
            with open("user_input.txt", "r") as f:
                saved_input = f.read()
            st.write("Saved Input:", saved_input)
        except FileNotFoundError:
            st.warning("No input saved yet.")
    st.write(" Welcome to the Whatsapp Chat Analyzer!")


def about_page():
    custom_style = ' font-weight: bold; font-size: 56px; text-decoration: underline; '
    st.write(f"<span style='{custom_style}'>Whatsapp Chat Analyser</span>", unsafe_allow_html=True)

    st.write(" ")
    uploaded_file = st.file_uploader("choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
        st.dataframe(df)

        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.sidebar.selectbox("Show Analysis", user_list)

        if st.sidebar.button("Show Statistical_Analysis"):
            
            num_messages, words_count, links, result_df = helper.fetch_stats(selected_user, df)

            a1 , a2, a3, a4,  = st.columns(4)

            a1 = st.columns(1)
            with a1[0]:
                st.markdown(f"<h1 style='font-weight: bold; font-size: 40px;'>Total Messages: {num_messages}</h1>", unsafe_allow_html=True)

            a2 = st.columns(1)
            with a2[0]:
                st.markdown(f"<h1 style='font-weight: bold; font-size: 40px;'>Total Words: {words_count}</h1>", unsafe_allow_html=True)

            a3 = st.columns(1)
            with a3[0]:
                st.markdown(f"<h1 style='font-weight: bold; font-size: 40px;'>Total Links: {links}</h1>", unsafe_allow_html=True)


        if st.sidebar.button("Show Sentimental_Analysis"):

            if uploaded_file is not None:
                messages = uploaded_file.read().decode("utf-8")                
                analysis_results = perform_sentiment_analysis(messages, df)

                custom_style = 'font-weight: bold; font-size: 40px; text-decoration: underline; '
                st.write(f"<span style='{custom_style}'>Sentiment Analysis</span>", unsafe_allow_html=True)

                custom_style = 'color: green; font-weight: bold; font-size: 24px;'# Display the styled text
                st.write(f"<span style='{custom_style}'>Positive: {analysis_results['sentiment_scores']['pos']}</span>", unsafe_allow_html=True)

                custom_style = 'color: red; font-weight: bold; font-size: 24px;'# Display the styled text
                st.write(f"<span style='{custom_style}'>Negative: {analysis_results['sentiment_scores']['neg']}</span>", unsafe_allow_html=True)

                custom_style = 'color: blue; font-weight: bold; font-size: 24px;'# Display the styled text
                st.write(f"<span style='{custom_style}'>Neutral: {analysis_results['sentiment_scores']['neu']}</span>", unsafe_allow_html=True)

                custom_style = ' font-weight: bold; font-size: 40px; text-decoration: underline; '
                st.write(f"<span style='{custom_style}'>Overall Sentiment</span>", unsafe_allow_html=True)

                custom_style = 'color: blue; font-weight: bold; font-size: 32px; '
                st.write(f"<span style='{custom_style}'>{analysis_results['overall_sentiment']}</span>", unsafe_allow_html=True)

                custom_style = ' font-weight: bold; font-size: 40px; text-decoration: underline;'
                st.write(f"<span style='{custom_style}'> Most Common Words</span>", unsafe_allow_html=True)

                data = analysis_results["top_100_words"]
                df = pd.DataFrame(data, columns=["Content", "Count"])
                st.dataframe(df, width=400)

def thank_you():

    custom_style = ' font-weight: bold; font-size: 40px; text-decoration: underline;'
    st.write(f"<span style='{custom_style}'>About us </span>", unsafe_allow_html=True)


    # Define the information for the team members
    team_members = [
        {
            "name": "Riya Sharma",
            "roll_no": "21CE1375",
            "role": "Designer",
        },
        {
            "name": "Vishnu Gupta",
            "roll_no": "21CE1373",
            "role": "Tester",            
        },
        {
            "name": "Satwik Tripathi",
            "roll_no": "21CE1359",
            "role": "Tester",           
        },
        {
            "name": "Prathamesh Tripathi ",
            "roll_no": "21CE1038",
            "role": "Developer",            
        },
    ]
    # Create a layout to display team members
    for member in team_members:
        st.markdown(f"**Name:** {member['name']}")
        st.markdown(f"**Roll No:** {member['roll_no']}")
        st.markdown(f"**Role:** {member['role']}")
        st.write("------")
        
    st.header("Thank you for visiting Whatsapp Chat Analyzer for Investigation")


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a Page", ["Login", "Whatsapp Chat Analyser", "About"])

    if page == "Login": 
        homepage()
    elif page == "Whatsapp Chat Analyser":
        about_page()
    else:
        page == "About "
        thank_you()

if __name__ == "__main__":
    main()

