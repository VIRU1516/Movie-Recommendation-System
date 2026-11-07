import os
import pickle
import time

import requests
import streamlit as st

st.set_page_config(page_title="MoviesForYou", page_icon="🎬", layout="wide")

# ---------- Config ----------
# The OMDb API key is read from Streamlit secrets or an environment variable.
# It is never stored in the code, so this file is safe to publish.
try:
    OMDB_KEY = st.secrets["OMDB_KEY"]
except Exception:
    OMDB_KEY = os.getenv("OMDB_KEY", "")

PLACEHOLDER = "https://placehold.co/500x750/141414/e50914?text=No+Poster"

# ---------- Styling ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600&display=swap');
#MainMenu, footer, header {visibility: hidden;}
h1, h2, h3, h4, p, label, [data-testid="stWidgetLabel"] p, [data-testid="stCaptionContainer"],
[data-testid="stMarkdownContainer"] {color: #ffffff !important;}
.stApp {background: radial-gradient(circle at top, #2a0a0d 0%, #0b0b0b 55%); color: #fff; font-family: 'Inter', sans-serif;}
.brand {font-family: 'Bebas Neue', sans-serif; color: #e50914; letter-spacing: 4px; text-align: center; font-size: 4.5rem; margin: 0;}
.sub {text-align: center; color: #b3b3b3 !important; margin-bottom: 1.5rem;}
.splash {height: 80vh; display: flex; align-items: center; justify-content: center; animation: pop 1.8s ease-in-out;}
@keyframes pop {0% {opacity: 0; transform: scale(.6);} 50% {opacity: 1; transform: scale(1.1);} 100% {opacity: 1; transform: scale(1);}}
.wordmark {font-family: 'Bebas Neue', sans-serif; color: #e50914; letter-spacing: 8px; font-size: 4rem; margin-top: 1rem;}
.card {background: rgba(255,255,255,0.06); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px; padding: 10px; transition: transform .25s, box-shadow .25s;}
.card:hover {transform: translateY(-6px); box-shadow: 0 10px 30px rgba(229,9,20,.45);}
.card img {width: 100%; border-radius: 10px;}
.card p {margin: 8px 0 2px; font-weight: 600; text-align: center; font-size: .95rem;}
.stButton > button {background: #e50914; color: #fff; border: none; border-radius: 8px; font-weight: 600; padding: .5rem 1.6rem;}
.stButton > button:hover {background: #b20710; color: #fff;}
</style>
""",
    unsafe_allow_html=True,
)


# ---------- Logo ----------
def logo(size=100):
    return (
        '<svg width="%d" height="%d" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        '<rect x="5" y="5" width="90" height="90" rx="22" fill="#e50914"/>'
        '<polygon points="40,28 40,72 74,50" fill="#ffffff"/></svg>' % (size, size)
    )


# ---------- Splash screen (shown once per session) ----------
if "splash_done" not in st.session_state:
    ph = st.empty()
    ph.markdown(
        '<div class="splash"><div style="text-align:center">' + logo(150)
        + '<div class="wordmark">MOVIESFORYOU</div></div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(2.5)
    ph.empty()
    st.session_state.splash_done = True


# ---------- Data loading and recommendation logic ----------
@st.cache_resource(show_spinner="Loading movies...")
def load_data():
    movies = pickle.load(open("movie_list.pkl", "rb")).reset_index(drop=True)
    neighbors = pickle.load(open("neighbors.pkl", "rb"))  # top-10 similar movie indices per movie
    return movies, neighbors


def _get_poster(title):
    r = requests.get("http://www.omdbapi.com/", params={"apikey": OMDB_KEY, "t": title}, timeout=5)
    r.raise_for_status()
    poster = r.json().get("Poster")
    return poster if poster and poster != "N/A" else PLACEHOLDER


@st.cache_data(show_spinner=False)
def _cached_poster(title):
    return _get_poster(title)


def fetch_poster(title):
    try:
        return _cached_poster(title)
    except Exception:
        return PLACEHOLDER


def recommend(title, n):
    idx = movies[movies["title"] == title].index[0]
    return [movies.iloc[i].title for i in neighbors[idx][:n]]


movies, neighbors = load_data()

# ---------- Main page ----------
st.markdown('<div style="text-align:center">' + logo(80) + "</div>", unsafe_allow_html=True)
st.markdown('<p class="brand">MOVIESFORYOU</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">Pick a movie you love. We\'ll find what to watch next.</p>', unsafe_allow_html=True)

if not OMDB_KEY:
    st.warning("OMDb API key not found, so posters will not be shown. "
               "Add OMDB_KEY to .streamlit/secrets.toml.")

selected = st.selectbox("Search a movie", movies["title"].values, index=None,
                        placeholder="Type a movie name...")
n = st.slider("How many recommendations?", 5, 10, 5)

if st.button("Recommend") and selected:
    with st.spinner("Finding movies for you..."):
        recs = recommend(selected, n)
    st.subheader(f"Because you liked {selected}")
    for start in range(0, len(recs), 5):
        cols = st.columns(5)
        for col, t in zip(cols, recs[start : start + 5]):
            with col:
                st.markdown(
                    f'<div class="card"><img src="{fetch_poster(t)}"><p>{t}</p></div>',
                    unsafe_allow_html=True,
                )
elif not selected:
    st.caption("Select a movie above and press Recommend.")