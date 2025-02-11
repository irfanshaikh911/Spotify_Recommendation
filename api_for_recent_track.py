import requests
from flask import Flask, request, redirect

# 🔹 Replace with your Spotify API credentials
CLIENT_ID = '28db5fc87989410e902ef68a0db47acc'
CLIENT_SECRET = 'bfae59fa5e724e0abce5a402ea748fac'
REDIRECT_URI = "http://localhost:5000/callback"  # Must match your Spotify Developer Dashboard
SCOPES = "user-read-recently-played user-library-read user-read-private"

# 🔹 Spotify API URLs
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

# 🔹 Initialize Flask app
app = Flask(__name__)

# 🔹 Step 1: Redirect user to Spotify login
@app.route("/")
def login():
    auth_query_parameters = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES
    }
    auth_url = f"{AUTH_URL}?{requests.compat.urlencode(auth_query_parameters)}"
    return redirect(auth_url)

# 🔹 Step 2: Handle the redirect and get the access token
@app.route("/callback")
def callback():
    code = request.args.get("code")  # Get the authorization code from the URL
    
    # 🔹 Step 3: Exchange the authorization code for an access token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=token_data)
    token_json = response.json()

    if "access_token" in token_json:
        access_token = token_json["access_token"]
        return fetch_recently_played(access_token)
    else:
        return f"Error: {token_json}"

# 🔹 Step 4: Fetch Recently Played Songs using the Access Token
def fetch_recently_played(access_token):
    url = f"{API_BASE_URL}/me/player/recently-played?limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tracks = response.json()["items"]
        result = "<h2>🎵 Recently Played Tracks 🎵</h2><ul>"
        for track in tracks:
            track_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]
            result += f"<li>{track_name} - {artist_name}</li>"
        result += "</ul>"
        return result
    else:
        return f"Error: {response.json()}"

# 🔹 Run Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
