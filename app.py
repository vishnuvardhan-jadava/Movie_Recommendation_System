# importing all the required libraries

import streamlit as sl
import pickle
import requests


# we use this function to return the movie poster for the given movie_id.
def fetch_poster(id):
    ''' This function takes the movie_id given by the user and returns the image path using the TMDB official api'''
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=4477c8b9dd6f7ef02a3ca3be5abfa767&language=en-US'.format(id))
    # above api is an official property of TMDB www.themoviedb.org
    data = response.json()
    print(data)
    # returning the poster path for a given movie id
    return 'https://image.tmdb.org/t/p/original/' + data['poster_path']


def recommend(movie):
    '''This function takes the movie title and recommends the related movies'''
    c = 0
    for i in movies_list:
        if movie == i:
            index = c
            break
        c += 1
    distances = similarity[index]
    recommendations = []
    posters = []
    # sorting the top 5 related and recommended movies for the given movie name
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies:
        movie_id = movie_ids[i[0]]
        recommendations.append(movies_list[i[0]])
        posters.append(fetch_poster(movie_id))
    # The above loop appends the recommended movies to recommendations list and posters to posters list respectively
    return recommendations, posters


# Using the pickle library to convert the pkl file into dataframe and using it to load to list of values
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = pickle.load(open('movies.pkl', 'rb'))

# creating the separate lists containing movie titles and movie ids
movie_ids = movies_list['movie_id'].values
movies_list = movies_list['title'].values

# Title page of the application
sl.title('Movie Recommendation System')

# user dropdown with movies list
selected_movie = sl.selectbox('Give us a movie', movies_list)

# Displaying the results on button press
if sl.button('Recommend'):
    recommendations, posters = recommend(selected_movie)
    col1, col2, col3 = sl.columns(3)
    with col1:
        sl.text(recommendations[0])
        sl.image(posters[0])
    with col2:
        sl.text(recommendations[1])
        sl.image(posters[1])
    with col3:
        sl.text(recommendations[2])
        sl.image(posters[2])
    col4, col5, col6 = sl.columns(3)
    with col4:
        sl.text(recommendations[3])
        sl.image(posters[3])
    with col5:
        sl.text(recommendations[4])
        sl.image(posters[4])

# Loading the dictionary values with key as movie id and value as popularity index using pickle
pop = pickle.load(open('popular_movies.pkl', 'rb'))

# Creating separate lists to store popular movie ids and their values
pop_movie = []
pop_title = []

# appending the results using the loaded dictionary to the lists
for i, j in pop.items():
    pop_movie.append(i)
    pop_title.append(j)


# Creating a function which returns popular movie names and their poster paths given the ids of that particular movie
def popular_movies_viewer(pop_movie):
    pop_movie = pop_movie
    pop_movie_posters = []
    for i in pop_movie:
        pop_movie_posters.append(fetch_poster(i))
    return pop_movie, pop_movie_posters


# Header for popular movie results section on the application page
sl.header('Other Popular Movies you may like')

# Displaying the results of popular movie names and posters obtained by previous function call
pop_mv, popular = popular_movies_viewer(pop_movie)
col1, col2, col3, col4, col5 = sl.columns(5)

with col1:
    sl.text(pop[pop_mv[0]])
    sl.image(popular[0])
with col2:
    sl.text(pop[pop_mv[1]])
    sl.image(popular[1])
with col3:
    sl.text(pop[pop_mv[2]])
    sl.image(popular[2])
with col4:
    sl.text(pop[pop_mv[3]])
    sl.image(popular[3])
with col5:
    sl.text(pop[pop_mv[4]])
    sl.image(popular[4])
