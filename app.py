import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY=os.getenv("openai_api_key")
client = OpenAI(api_key=API_KEY)


if "modelName" not in st.session_state:
    st.session_state.modelName="ft:gpt-3.5-turbo-1106:group-c:faketweetgen:9KbObRP4"

if "tweets" not in st.session_state:
    st.session_state.tweets=[]

if "Sentiment" not in st.session_state:
    st.session_state.Sentiment=[]

if "positive" not in st.session_state:
    st.session_state.positive=0
if "negative" not in st.session_state:
    st.session_state.negative=0
if "neutral" not in st.session_state:
    st.session_state.neutral=0


@st.cache_resource()
def GetTweets(certain,product,modelName):
    returnable=[]
    while certain >0:

        completion = client.chat.completions.create(
        model=f"{modelName}",
        messages=[
    {"role": "system", "content": "You Are a Fake Tweet generator that generates fake tweets about a product just based of a product name"},
    {"role": "user", "content": f"{product}"}
                ]
                )
        returnable.append(completion.choices[0].message.content)
        certain=certain-1

    return returnable

@st.cache_resource()
def sentimentAnalyzer(userMessage):
    returnable=''

 
    completion=client.chat.completions.create(
    model="ft:gpt-3.5-turbo-1106:group-c:twittersentiment:9Kb2JaYK",
    messages=[
    {"role": "system", "content": "You Are A Brand Sentiment analysis chatbot that analyses tweets and provides an analysis on the sentiment from the tweet"},
    {"role": "user", "content": f"{userMessage}"}]
   
    )
    returnable = completion.choices[0].message.content

    return returnable


def count_emotion():
    import re
    for index in range(len(st.session_state.Sentiment)):
        emotion_match = re.search(r"'Emotion:',\s*(.*)", st.session_state.Sentiment[index])
        if emotion_match:
            emotion = emotion_match.group(1)
        if emotion =='Positive emotion':
            st.session_state.positive=st.session_state.positive +1
            print(st.session_state.positive)
        if emotion =='No emotion toward brand or product':
            st.session_state.neutral=st.session_state.neutral +1
            print('neutral')

        if emotion =='Negative emotion':
            st.session_state.negative=st.session_state.negative +1
            print('negative')



def analyze():
    
    st.session_state.tweets=[]
    st.session_state.Sentiment=[]
    st.session_state.positive=0
    st.session_state.negative=0
    st.session_state.neutral=0
    st.session_state.tweets=GetTweets(certain=st.session_state.number_of_tweets,product=st.session_state.brand,modelName=st.session_state.modelName)
    for tweets in st.session_state.tweets:
        sentiment=sentimentAnalyzer(tweets)
        

        st.session_state.Sentiment.append(sentiment)
    count_emotion()

    
    




st.set_page_config(page_title="Using tweets for sentiment analysis on brands")

st.title("Brand Sentiment Analysis")
with st.form("form"):
    st.text_input(label='Enter Brand Name',autocomplete='Apple',key='brand')
    st.slider(
        label="How many Tweets should be used",
        min_value=1,
        max_value=40,
        step=1,
        key="number_of_tweets"
    )
    st.form_submit_button('Analyze',on_click=analyze)


st.write(st.session_state.brand)



Generated_Tweets,Tweets_and_emotions,Graphical_Rep=st.tabs(["Generated Tweets","Tweets And Sentiment Analysis","Graphical Representation"])


with Generated_Tweets:
    for tweets in st.session_state.tweets:
        st.code(f" {tweets}")

with Tweets_and_emotions:
    for index in range(len(st.session_state.Sentiment)):
        st.write(f"{st.session_state.tweets[index]}")
        st.code({st.session_state.Sentiment[index]})
        




with Graphical_Rep:
    import pandas as pd
    import numpy as np
    
    
    # Sample data
    data = pd.DataFrame({
        'Category': ['No emotion toward brand or product', 'Positive Emotion', 'Negative Emotion'],
        'Values': [st.session_state.neutral, st.session_state.positive, st.session_state.negative]
    })

    # Create a bar chart
    st.bar_chart(data.set_index('Category'))

    # Alternatively, you can use a list of values
    # values = [10, 20, 30, 40]
    # st.bar_chart(values)
