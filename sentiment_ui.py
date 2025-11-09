import streamlit as st
from textblob import TextBlob

def sentiment_panel():
    st.subheader("💬 Customer Review Sentiment")
    text = st.text_area("Write or paste a customer review here:")
    if st.button("Analyze Sentiment"):
        if text.strip():
            polarity = TextBlob(text).sentiment.polarity
            if polarity > 0.2:
                st.success("😊 Positive Review")
            elif polarity < -0.2:
                st.error("😞 Negative Review")
            else:
                st.info("😐 Neutral Review")
        else:
            st.warning("Please enter some text.")