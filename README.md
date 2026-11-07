#  MoviesForYou

A content-based movie recommendation web app built with Python and Streamlit.
Pick a movie you like and get 5 to 10 similar movies, shown as Netflix-style poster cards.

## Features

- Search any of ~4,800 movies from the TMDB 5000 dataset
- Choose how many recommendations you want (5 to 10)
- Movie posters fetched from the OMDb API
- Dark, Netflix-inspired interface with a splash screen

## Screenshots

| Search | Recommendations |
|---|---|
| ![Movie search](screenshots/movie_search.png) | ![Recommendations](screenshots/recommendation.png) |

## How it works

1. `movies` and `credits` data are merged and cleaned (overview, genres, keywords, top 3 cast, director).
2. These fields are combined into one `tags` text per movie.
3. `CountVectorizer` (5,000 features) turns each `tags` text into a vector.
4. Cosine similarity compares every movie with every other movie.
5. For each movie, the 10 most similar movies are saved in `neighbors.pkl`, and the app looks them up instantly.

The full model-building process is in `PrepFinal.ipynb`.

## Tech stack

Python, Pandas, NumPy, scikit-learn, Streamlit, OMDb API

## Run it locally

```bash
git clone <your-repo-url>
cd MoviesForYou
python -m venv .venv
.venv\Scripts\activate        # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

Get a free API key from [omdbapi.com](https://www.omdbapi.com/apikey.aspx), then create the file
`.streamlit/secrets.toml` with this line:

```toml
OMDB_KEY = "your_key_here"
```

Start the app:

```bash
streamlit run app.py
```

Without a key the app still works, but posters are replaced by placeholders.

## Rebuild the model (optional)

1. Download the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`) into the project folder.
2. Run all cells in `PrepFinal.ipynb` to create `movie_list.pkl` and `similarity.pkl`.
3. Run `python make_neighbors.py` to create the small `neighbors.pkl` that the app uses.

## Acknowledgements

The core recommendation approach (content-based filtering with `CountVectorizer` and cosine similarity on the
TMDB 5000 dataset) was learned from the CampusX YouTube channel's movie recommender system tutorial.
I built the Streamlit interface, the OMDb poster integration, the splash screen and the compact
`neighbors.pkl` optimisation on top of it.

## Author

Viraj, BCA student
