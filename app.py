from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():

    recommendations = []

    if request.method == 'POST':

        selected_movie = request.form.get('movie')

        if selected_movie:
            recommendations = recommend(selected_movie)

    return render_template(
        'index.html',
        recommendations=recommendations
    )

if __name__ == '__main__':
    app.run(debug=True)