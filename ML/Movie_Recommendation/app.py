import pickle
import requests
import streamlit as st

#Page configs

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Design
st.markdown("""
<style>

.stApp {
    background-color: #141414;
}

/* Title */
.main-title {
    text-align: center;
    color: #E50914;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 30px;
}

/* Movie names */
.movie-title {
    text-align: center;
    color: white;
    font-size: 16px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* Button */
div[data-testid="stButton"] button {
    width: 100%;
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    border: none;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

div[data-testid="stButton"] button:hover {
    background-color: #B20710;
    color: white;
}

/* Selectbox label */
label {
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

/* Images */
img {
    border-radius: 12px;
    transition: all 0.3s ease;
}

img:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# Functions
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movie_names, recommended_movie_posters


# Data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown(
    '<div class="main-title">🎬 Movie Recommender System</div>',
    unsafe_allow_html=True
)

st.write("")

# Selection and Recommendation
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Choose a movie",
    movie_list
)

if st.button("🍿 Show Recommendations"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], use_container_width=True)
        st.markdown(
            f'<div class="movie-title">{names[0]}</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.image(posters[1], use_container_width=True)
        st.markdown(
            f'<div class="movie-title">{names[1]}</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.image(posters[2], use_container_width=True)
        st.markdown(
            f'<div class="movie-title">{names[2]}</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.image(posters[3], use_container_width=True)
        st.markdown(
            f'<div class="movie-title">{names[3]}</div>',
            unsafe_allow_html=True
        )

    with col5:
        st.image(posters[4], use_container_width=True)
        st.markdown(
            f'<div class="movie-title">{names[4]}</div>',
            unsafe_allow_html=True
        )