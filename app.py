from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

TMDB_API_KEY = "7790fcf770dfc0a830dfa82c8817eb90"  
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form.get("movie")
        if search_query:
            return redirect(url_for('movie_browse', query=search_query))
    return render_template("index.html")

@app.route("/browse", methods=["GET"])
def movie_browse():
    search_query = request.args.get("query", "")
    movies = []

    if search_query:
        params = {"api_key": TMDB_API_KEY, "query": search_query}
        response = requests.get(TMDB_SEARCH_URL, params=params)
        if response.status_code == 200:
            movies = response.json().get("results", [])

    return render_template("movie-browse.html", movies=movies, search_query=search_query)


@app.route("/info/<int:movie_id>")
def movie_info(movie_id):

    search_query = request.args.get('search_query')

    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", params={"api_key": TMDB_API_KEY})
    movie = response.json() if response.status_code == 200 else {}
    similar_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={TMDB_API_KEY}&language=en-US")
    if similar_response.status_code == 200:
        similar_movies = similar_response.json().get("results", [])
    else:
        print("Error fetching similar movies.")

    trailer_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos", params={"api_key": TMDB_API_KEY})
    videos = trailer_response.json().get("results", [])

    

    trailer_url = ""
    for video in videos:
        if video["type"] == "Trailer":
            trailer_url = f"https://www.youtube.com/embed/{video['key']}"
            break

    return render_template("movie_info.html", movie=movie, trailer_url=trailer_url, similar_movies=similar_movies, search_query=search_query)
    
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
