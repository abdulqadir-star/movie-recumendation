import streamlit as st
import pickle
import pandas as pd
import gzip

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: gray;
    }
    </style>
    <div class="footer">Developed by Ansari</div>
    """,
    unsafe_allow_html=True
)

# Page config (optional)
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
# similarity = pickle.load(open("similarity.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"), encoding="latin1")
# with gzip.open("similarity.pkl.gz", "wb") as f:
#     pickle.dump(similarity, f)
#     similarity = pickle.load(f)
# Simple CSS to change only the overall screen background
st.markdown("""
<style>
    /* Change the main background color */
    .stApp {
        background-color: #f0f2f9;
    }
    /* Optional: change title color if you like */
    .stTitle {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movies Recommended")

def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

option = st.selectbox("What do you want to see", movies['title'].values)

if st.button('Recommended'):
    recommendations = recommended(option)
    st.write("### Top 5 recommendations:")
    for i, movie in enumerate(recommendations, start=1):
        st.write(f"{i}. {movie}")

st.markdown('<div class="footer">Developed by Ansari</div>', unsafe_allow_html=True)        
