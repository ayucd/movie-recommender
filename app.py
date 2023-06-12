import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5f5d339657562895434436581f43f22c'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

#function that recommends top 5 movies
def recommend(movie):
  #fetch the index of movie from data
  movie_index=movies[movies['title']==movie].index[0]
  #fetching the array corresponding to the movie in similarity matrix
  distances=similarity[movie_index]
  #sorting and ordering to get top 5
  movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  recommended_movies=[]
  recommended_movie_posters=[]
  for i in movie_list:
      movie_id=movies.iloc[i[0]].movie_id
      recommended_movies.append(movies.iloc[i[0]].title)
      #fetching posters from api
      recommended_movie_posters.append(fetch_poster(movie_id))
  return recommended_movies,recommended_movie_posters

movies_list=pickle.load(open('movies.pkl', 'rb'))
movies=pd.DataFrame(movies_list)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

select_movie = st.selectbox(
'Select a movie of your choice!',
movies['title'].values)

if st.button('Recommend'):
    names,posters=recommend(select_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

