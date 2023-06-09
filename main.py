from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    category = request.form['category']
    mood = request.form['mood']
    time_period = request.form['time_period']

    movies_df = pd.read_csv('tmdb_5000_movies.csv')

    if time_period == '80ler':
        year_start = 1980
        year_end = 1989
    elif time_period == '90lar':
        year_start = 1990
        year_end = 1999
    elif time_period == '2000ler':
        year_start = 2000
        year_end = 2009
    elif time_period == '2010lar':
        year_start = 2010
        year_end = 2023
    else:
        year_start = None
        year_end = None

    if year_start and year_end:
        selected_movies = movies_df[((movies_df['genres'].str.contains(category)) & (movies_df['release_date'].str[:4].astype(float) >= year_start) & (movies_df['release_date'].str[:4].astype(float) <= year_end)) | (movies_df['overview'].str.contains(mood, case=False))]
    else:
        selected_movies = movies_df[(movies_df['genres'].str.contains(category)) | (movies_df['overview'].str.contains(mood, case=False))]

    recommended_movies = selected_movies.sort_values('popularity', ascending=False)[:12]

    return render_template('recommend.html', movies=recommended_movies['title'])


if __name__ == '__main__':
    app.run(debug=True)#