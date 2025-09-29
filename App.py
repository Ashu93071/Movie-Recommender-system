import streamlit as st
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import requests,time

API_key="4b0b2c7ec74a8948dfee25859a994f48"

#importing our saved model.
movies_list=pickle.load(open('movies.pkl', 'rb'))
movies=movies_list['title'].values
vectors=pickle.load(open('vectors.pkl', 'rb'))
new_df=pickle.load(open('DataFrame.pkl','rb'))

# Creating a var for tmdb server handling for poster extraction.
def fetch_poster(movie_id, retries=3, backoff=1):
    """Fetch poster URL from TMDB with retries + caching."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_key}&language=en-US"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return None
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(backoff * (2 ** attempt))  # exponential backoff
            else:
                st.error(f"Failed to fetch poster for {movie_id}: {e}")
                return None


sim = cosine_similarity(vectors)
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    dist = sim[movie_index]
    sort = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in sort:
        movie_id=new_df.iloc[i[0]].id
        five_movies = new_df.iloc[i[0]].title
        recommended_movies.append(five_movies)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

st.title('Movie Recommender System')
option = st.selectbox(
    "Select the movies for which you would like to recommend",
    movies)


#for options:
if st.button("Recommend"):
    recommendations, posters = recommend(option)
    #for poster display:
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
         st.text(recommendations[2])
         st.image(posters[2])

    with col4:
         st.text(recommendations[3])
         st.image(posters[3])

    with col5:
         st.text(recommendations[4])
         st.image(posters[4])