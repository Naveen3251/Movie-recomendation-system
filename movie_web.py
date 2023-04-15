import streamlit as st
import pickle
import pandas as pd
#to get API request
import requests
#defining recommend function

#loading the movie data pickle file
movie_dict=pickle.load(open('Movies_dict.pkl','rb'))

#loading cosine sumilarity file
similarity=pickle.load(open('cosine_similarity.pkl','rb'))
#converting dict file to data frame
movies=pd.DataFrame(movie_dict)

#to fetch posters from tmdb api
def fetch_poster(movie_id):
    data=None
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=284e51615e9252a13a028cd59ef391d7'.format(movie_id))
        data = response.json()
    except:
        st.write("Check out Internet connectivity to display a poster")


    if data is not None and data.get('poster_path'):
        return "http://image.tmdb.org/t/p/w185/"+data['poster_path']
    else:
        return "https://via.placeholder.com/185x278.png?text=Poster+Not+Available"




def recommend(movie):
       #to get the movie index
        movie_index=movies[movies['title']==movie].index[0]
        #distances
        distance=similarity[movie_index]
        movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
        recommended_movie=[]
        recomended_movies_poster=[]
        for i in movie_list:
            #to get movie id
            movie_id=movies.iloc[i[0]].id
            recommended_movie.append(movies.iloc[i[0]].title)
            # fetching poster from  tmdb API
            #passing only id
            recomended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movie,recomended_movies_poster



st.title('MOVIE WEB')
#to select list of movies in select box
selected_movie_name=st.selectbox('How would you like to be connected?', movies['title'].values)

if st.button('Recommend'):
    recomendations,posters=recommend(selected_movie_name)
    #to display images->layout
    col1,col2,col3=st.columns(3)
    col4, col5=st.columns(2)
    with col1:
        if recomendations:
            st.text(recomendations[0])
            st.image(posters[0])
    with col2:
        if recomendations:
            st.text(recomendations[1])
            st.image(posters[1])
    with col3:
        if recomendations:
            st.text(recomendations[2])
            st.image(posters[2])
    with col4:
        if recomendations:
            st.text(recomendations[3])
            st.image(posters[3])
    with col5:
        if recomendations:
            st.text(recomendations[4])
            st.image(posters[4])
