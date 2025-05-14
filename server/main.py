from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode
import httpx
import os

from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace these with your actual Spotify credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
LRCLIB_URL = "https://lrclib.net/api/get"

# Temporary in-memory storage (use a database or sessions in production)


@app.get("/auth/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-currently-playing",
    }
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(auth_url)


@app.get("/callback")
async def callback(request: Request):

    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback.")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(SPOTIFY_TOKEN_URL, data=data)

    if token_response.status_code != 200:
        raise HTTPException(status_code=token_response.status_code, detail="Failed to get access token.")

    token_json = token_response.json()
    ACCESS_TOKEN = token_json["access_token"]

    return JSONResponse(content={"message": "Authentication successful!", "access_token": ACCESS_TOKEN})


@app.get("/current-track")
async def get_current_track(ACCESS_TOKEN: str = None):
    if not ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(SPOTIFY_CURRENT_TRACK_URL, headers=headers)

    if response.status_code == 204:
        raise HTTPException(status_code=404, detail="No song currently playing.")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching current track.")

    track_data = response.json()
    item = track_data["item"]
    return {
        "artists": item["artists"],
        "track": item["name"],
        "album": item["album"]["name"],
        "duration": item["duration_ms"] // 1000,
        "progress": track_data["progress_ms"] // 1000,
        "is_playing": track_data["is_playing"],
        "song_img": item["album"]["images"][0]["url"],
    }


@app.get("/lyrics")
async def get_lyrics(artist: str, track: str, ACCESS_TOKEN: str = None):
    if not ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    # Get current track first
    headers = {"User-Agent": "LRCGET v0.2.0 (https://github.com/tranxuanthang/lrcget)"}

    req = requests.get(f"https://lrclib.net/api/get?artist_name={artist}&track_name={track}", headers=headers, timeout=5)
    if req.status_code != 200:
        raise HTTPException(status_code=req.status_code, detail="Error fetching lyrics.")
    
    lyrics_data = req.json()
    print(lyrics_data)
    
    return lyrics_data["syncedLyrics"]
