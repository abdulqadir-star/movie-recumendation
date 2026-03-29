import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Page config must be first Streamlit command
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# Custom CSS for background color and footer
st.markdown(
    """
    <style>
    /* Change main background color */
    .stApp {
        background-color: #f0f2f9;
    }
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Movies Recommended")

# Load movies data (must be in the same directory)
movies = pickle.load(open("movies.pkl", "rb"))

# Google Drive file ID (extracted from your link)
FILE_ID = "1vE367IR4oNQcXbll-VKHgzU2iI9ZMLbf"
OUTPUT_PATH = "similarity.pkl"

# Download similarity.pkl if not already present
if not os.path.exists(OUTPUT_PATH):
    with st.spinner("Downloading similarity data (large file)... Please wait."):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, OUTPUT_PATH, quiet=False)
    st.success("Download complete!")

# Load similarity matrix
with open(OUTPUT_PATH, "rb") as f:
    similarity = pickle.load(f)

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

# Footer
st.markdown('<div class="footer">Developed by Ansari</div>', unsafe_allow_html=True)
