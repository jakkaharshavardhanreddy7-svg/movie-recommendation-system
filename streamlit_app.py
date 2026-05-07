import streamlit as st
import pickle

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie = movie.lower()

    matches = movies[movies['title'].str.lower() == movie]

    if matches.empty:
        return ["Movie not found"]

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Movie Recommendation System")

movie_name = st.text_input("Enter Movie Name")

if st.button("Recommend"):

    recommendations = recommend(movie_name)

    st.subheader("Recommended Movies")

    for movie in recommendations:
        st.write("✅", movie)