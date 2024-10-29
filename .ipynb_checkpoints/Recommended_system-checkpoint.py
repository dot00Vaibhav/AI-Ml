import streamlit as st
import pandas as pd

# Load data
books = pd.read_csv('books.csv')
ratings = pd.read_csv('ratings.csv')

# Process data
ratings_with_name = ratings.merge(books, on='ISBN')
num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].agg(lambda x: x.astype(float).mean()).reset_index()
avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)

popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')
popular_df = popular_df[popular_df['num_ratings'] >= 250].sort_values('avg_rating', ascending=False).merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'avg_rating']]

def recommend_books(book_title):
    recommendations = popular_df[popular_df['Book-Title'].str.contains(book_title, case=False)]
    if recommendations.empty:
        recommendations = popular_df.head(5)  # Show top 5 if no match found
    return recommendations

# Streamlit App
st.title("Book Recommendation System")

book_title = st.text_input("Enter a book title to get recommendations:")
search_button = st.button("Search")

if search_button:
    if book_title:
        recommended_books = recommend_books(book_title)
        
        st.write("Recommendations:")
        for index, row in recommended_books.iterrows():
            st.subheader(row['Book-Title'])
            st.write(f"Author: {row['Book-Author']}")
            st.write(f"Average Rating: {row['avg_rating']:.2f}")
            st.write(f"Number of Ratings: {row['num_ratings']}")
            st.image(row['Image-URL-M'])
    else:
        st.warning("Please enter a book title to search.")
