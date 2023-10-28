import streamlit as st
import pickle
import pandas as pd
import requests
import zipfile
import json
import joblib
from streamlit_lottie import st_lottie 


st.set_page_config(
    page_title="Movie Recommandation App Using ML 📽️🍿",
    layout="wide",  # Set the layout to wide mode
)

path = "Movies.json"
with open(path,"r") as file: 
    url = json.load(file)

col1, col2 = st.columns(2)

with col1:
    st.title("Movie Recommendation App Using Machine Learning")

with col2:
    st_lottie(url, 
        reverse=True, 
        height=400, 
        width=400, 
        speed=1, 
        loop=True,
    )


# movies = pickle.load(open('movie_list.pkl','rb'))
with open('movie_list.pkl', 'rb') as file:
    movies = joblib.load(file)

# similarity = pickle.load(open('similarity.pkl','rb'))


zip_file_path = "similarity_compre.zip"
pickle_file_name = "similarity.pkl"

with zipfile.ZipFile(zip_file_path, "r") as zip_file:
    # Extract the pickle file from the ZIP archive
    with zip_file.open(pickle_file_name) as pickle_file:
        # Load the data from the pickle file
        similarity = pickle.load(pickle_file)


new_df = pd.read_csv('new_df_tags.csv')
main_tags_df = pd.DataFrame(new_df)

# Funtions --------------

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=be04bc9e87e0b0b6ad863f307c4f55cf&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend_movies(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:7]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        # print(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


def recommend_directors(movie):
    directors_movies = main_tags_df[main_tags_df["tags"].str.contains(selected_name)]

    # st.write(directors_movies)

    directors_movies_df = pd.DataFrame(directors_movies)

    recommended_movie_names = []
    recommended_movie_posters = []

    for index, row in directors_movies_df.iterrows():
        movie_id = row["movie_id"]
        # st.write(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        movie_name = movies.loc[movies['movie_id'] == movie_id, 'title'].values[0]

        recommended_movie_names.append(movie_name)

    return recommended_movie_names,recommended_movie_posters

# Create a sidebar for navigation
navigation = st.sidebar.selectbox("Main Menu", ["Movies", "Directors"])


# Display content based on navigation selection
if navigation == "Movies":
    st.header("Please Select and See Similar Movies 📽️")
    # You can add content specific to the 'Movies' button here.

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type Or Select A Movie From The Dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names,recommended_movie_posters = recommend_movies(selected_movie)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])

        col4, col5, col6 = st.columns(3)

        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
        with col6:
            st.text(recommended_movie_names[5])
            st.image(recommended_movie_posters[5])


elif navigation == "Directors":
    # page_content.text(page2_content)
    st.header("Explore Movies a/c To Directors 👩🏻‍💼")
    selected_name = st.selectbox("Select Your Favorite Director Name:", 
    [
    "JonFavreau", 
    "JamesGunn", 
    "JamesCameron", 
    "ChristopherNolan", 
    "PeterJackson",
    "RichardLinklater"]
    )

    if st.button("Show Movies"):
        directors_movies = main_tags_df[main_tags_df["tags"].str.contains(selected_name)]

        # Extract movie names
        movie_names = directors_movies["title"]

        # Display the movie names
        # if not movie_names.empty:
        #     print("Movies directed by James Cameron:")
        #     for movie_name in movie_names:
        #         print(Done)
        # else:
        #     print("No movies directed by James Cameron found.")

        recommended_movie_names, recommended_movie_posters = recommend_directors(selected_name)

        # recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])

        col4, col5, col6 = st.columns(3)

        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
        with col6:
            st.text(recommended_movie_names[5])
            st.image(recommended_movie_posters[5])


with st.sidebar:
    st.markdown('<div style="height:400px;"></div>', unsafe_allow_html=True)
    st.write("@ Copyrights Reserve to Bhupesh Kumar Dewangan 2023")

# else:
#     # page_content.text(page3_content)
#     st.header("Explore Movies a/c To Directors")
#     selected_name = st.selectbox("Select a name:", ["Sci-fi", "Adventure", "Nolan"])

#     if st.button("Show Movies"):
#         directors_movies = main_tags_df[main_tags_df["tags"].str.contains(selected_name)]

#         if len(directors_movies) > 6:
#             directors_movies = directors_movies[1:6]

#         # Extract movie names
#         movie_names = directors_movies["title"]

#         # Display the movie names
#         if not movie_names.empty:
#             print("Movies directed by James Cameron:")
#             for movie_name in movie_names:
#                 print(movie_name)
#         else:
#             print("No movies directed by James Cameron found.")

#         recommended_movie_names, recommended_movie_posters = recommend_directors(selected_name)

#         # recommended_movie_posters = recommend(selected_movie)
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.text(recommended_movie_names[0])
#             st.image(recommended_movie_posters[0])
#         with col2:
#             st.text(recommended_movie_names[1])
#             st.image(recommended_movie_posters[1])
#         with col3:
#             st.text(recommended_movie_names[2])
#             st.image(recommended_movie_posters[2])

#         col4, col5, col6 = st.columns(3)

#         with col4:
#             st.text(recommended_movie_names[3])
#             st.image(recommended_movie_posters[3])
#         with col5:
#             st.text(recommended_movie_names[4])
#             st.image(recommended_movie_posters[4])
#         with col6:
#             st.text(recommended_movie_names[5])
#             st.image(recommended_movie_posters[5])

