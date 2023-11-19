import pickle
import streamlit as st
import requests
import pandas as pd
import wikipedia

class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

import logging

# Function to fetch short summary from Wikipedia
def fetch_summary(movie_title):
    try:
        summary = wikipedia.summary(movie_title, sentences=1)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        logging.warning(f"DisambiguationError for movie {movie_title}: {e}")
        return "🚧 Sorry, there are multiple options for this movie."
    except wikipedia.exceptions.PageError as e:
        logging.warning(f"PageError for movie {movie_title}: {e}")
        return "📖 Sorry, Summary not found 😥😐."
    except Exception as e:
        logging.error(f"Error fetching summary for movie {movie_title}: {e}")
        return "⚠️ An unexpected error occurred while fetching the summary 🫤."


# Function to recommend movies with summaries
def recommend_with_summary(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []

    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        # Fetch the short summary from Wikipedia
        summary = fetch_summary(movie_title)
        recommended_movies.append({"title": movie_title, "summary": summary})

    return recommended_movies

# Load data
movies = pd.read_pickle(open('movie_list.pkl', 'rb'))
similarity = pd.read_pickle(open('similarity.pkl', 'rb'))

# Extract movie_list from the loaded data
movie_list = movies['title'].values

# Create or get the session state
session_state = SessionState(comments=[])

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Add custom CSS styles for color and animation
st.markdown(
    """
    <style>
    body {
        background-color: #ffc107; /* Yellow background */
        color: #333333;
    }
    .stApp {
        animation: fadeIn 2s;
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    .comment-section {
        background-color: #3498db; /* Updated color: Blue */
        color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content with color and animation
st.title('**Movie Recommender System**')
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Get user's name with colorful input box
user_name = st.text_input("👤 Your Name:", key='user_name', value="Anonymous")

# Movie selection dropdown with a colorful background
selected_movie = st.selectbox(
    "🎥 Select a movie:",
    movie_list,
    key='selected_movie',
    help="Choose a movie from the list."
)

# Button to show recommendations with a gradient background
if st.button('🍿 Show Recommendations'):
    recommended_movies_with_summary = recommend_with_summary(selected_movie)

    # Display recommendations with posters and summaries in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, data in enumerate(recommended_movies_with_summary):
        poster_path = fetch_poster(movies[movies['title'] == data['title']].iloc[0].movie_id)

        with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5:
            st.image(poster_path, use_column_width=True)

            # Create an expander for each movie summary
            with st.expander(f"{data['title']}", expanded=False):
                st.write(f"**{data['title']}**: {data['summary']}")


# Comment box for general comments with a colorful input area
user_comment_general = st.text_input("🗨️ Add your general comment:", key='user_comment_general')

# Button to post general comment with a gradient background
if st.button('✉️ Post General Comment') and user_comment_general and user_name:
    session_state.comments.append({"name": user_name, "comment": user_comment_general, "movie": None})

# Display comments with a colorful background
st.markdown('<div class="comment-section">', unsafe_allow_html=True)
st.title("📝 Comments")
for comment in session_state.comments:
    comment_movie = comment['movie'] if comment['movie'] else 'General'
    st.write(f"**{comment_movie}**: {comment['comment']} (by {comment['name'] if 'name' in comment else 'Anonymous'})")

# Create an expander for the project description in the right top corner
with st.sidebar:
    expander = st.expander("Project Description", expanded=False)
    expander.write("""
    This is a movie recommender system that suggests movies based on similarity scores calculated using a collaborative filtering algorithm. 
    Select a movie from the dropdown, click the "Show Recommendations" button, and explore the top five recommended movies along with their posters.

    The data is sourced from The Movie Database (TMDb) API, and the recommender system is built using Python, Streamlit, and machine learning techniques.

    Feel free to connect with me on GitHub or LinkedIn!
    """)

    # Animated GitHub and LinkedIn links with icons
    st.title('Connect with Me')

    # GitHub link with a different color
    st.markdown('<a href="https://github.com/ritesh1420" target="_blank" style="color: #ff5733;">'
                '<img src="https://img.shields.io/badge/GitHub-Profile-green?style=social&logo=github" alt="GitHub"></a>', 
                unsafe_allow_html=True)
    
    # LinkedIn link with a different color
    st.markdown('<a href="https://www.linkedin.com/in/ritesh-kumar~/" target="_blank" style="color: #3399FF;">'
                '<img src="https://img.shields.io/badge/LinkedIn-Profile-blue?style=social&logo=linkedin" alt="LinkedIn"></a>', 
                unsafe_allow_html=True)

# Close the divs
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
