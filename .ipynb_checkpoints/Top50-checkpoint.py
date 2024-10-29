# Top50.py

import streamlit as st
import pandas as pd
import pickle

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))

st.title("Top 50 Books")

#displaying books
num_books_per_row = 3
for i in range(0, len(popular_df), num_books_per_row):
    cols = st.columns(num_books_per_row)
    for j, col in enumerate(cols):
        if i + j < len(popular_df):
            book = popular_df.iloc[i + j]
            with col:
                st.image(book['Image-URL-M'], width=150)
                st.markdown(f"**Title:** {book['Book-Title']}")
                st.markdown(f"**Author:** {book['Book-Author']}")
                st.markdown(f"**Number of Ratings:** {book['num_ratings']}")
                st.markdown(f"**Average Rating:** {book['avg_rating']:.2f}")
                st.write("---")
