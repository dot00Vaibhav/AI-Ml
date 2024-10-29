import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
books = pd.read_pickle('books.pkl')
pt = pd.read_pickle('pt.pkl')
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Function to recommend books
def recommend(book_name):
    if book_name not in pt.index:
        return pd.DataFrame()  # Return an empty DataFrame if the book is not found
    
    # Find the index of the book
    index = np.where(pt.index == book_name)[0][0]
    
    # Get similarity scores for the book
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    # Prepare a list to store the recommended books
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    
    return pd.DataFrame(data, columns=['Book-Title', 'Book-Author', 'Image-URL-M'])

# Streamlit App
st.title("Book App")

# Navigation bar
nav = st.sidebar.radio("Navigation", ["Home", "Search"])

if nav == "Home":
    st.header("Top 50 Books")
    
    # Displaying books
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

elif nav == "Search":
    st.header("Book Recommendation System")
    
    book_title = st.text_input("Enter a book title to get recommendations:")
    search_button = st.button("Search")
    
    if search_button:
        if book_title:
            recommended_books = recommend(book_title)
            
            if not recommended_books.empty:
                st.write("Recommendations:")
                for index, row in recommended_books.iterrows():
                    st.subheader(row['Book-Title'])
                    st.write(f"Author: {row['Book-Author']}")
                    st.image(row['Image-URL-M'])
            else:
                st.write("No recommendations found. Try another book title.")
        else:
            st.warning("Please enter a book title to search.")
