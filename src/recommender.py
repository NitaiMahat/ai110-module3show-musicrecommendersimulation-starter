import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

DEFAULT_GENRE_WEIGHT = 2.0
DEFAULT_MOOD_WEIGHT = 1.0
DEFAULT_ENERGY_WEIGHT = 1.0
DEFAULT_VALENCE_WEIGHT = 1.0
DEFAULT_ACOUSTIC_BONUS = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by the current scoring recipe."""
        scored_songs = sorted(
            self.songs,
            key=lambda song: self._score_song_object(user, song)[0],
            reverse=True,
        )
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song was recommended for the given user."""
        _, reasons = self._score_song_object(user, song)
        return ", ".join(reasons)

    def _score_song_object(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "acousticness": song.acousticness,
        }
        return score_song(user_prefs, song_dict)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert numeric columns into Python numbers."""
    numeric_types = {
        "id": int,
        "energy": float,
        "tempo_bpm": float,
        "valence": float,
        "danceability": float,
        "acousticness": float,
    }
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            parsed_row: Dict = {}
            for key, value in row.items():
                converter = numeric_types.get(key)
                parsed_row[key] = converter(value) if converter else value
            songs.append(parsed_row)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song and return both the total and the reasons behind it."""
    score = 0.0
    reasons: List[str] = []
    genre_weight = float(user_prefs.get("genre_weight", DEFAULT_GENRE_WEIGHT))
    mood_weight = float(user_prefs.get("mood_weight", DEFAULT_MOOD_WEIGHT))
    energy_weight = float(user_prefs.get("energy_weight", DEFAULT_ENERGY_WEIGHT))
    valence_weight = float(user_prefs.get("valence_weight", DEFAULT_VALENCE_WEIGHT))
    acoustic_bonus = float(user_prefs.get("acoustic_bonus", DEFAULT_ACOUSTIC_BONUS))

    if song.get("genre") == user_prefs.get("genre"):
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    if song.get("mood") == user_prefs.get("mood"):
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None and song.get("energy") is not None:
        energy_similarity = max(0.0, 1 - abs(song["energy"] - target_energy))
        energy_points = energy_similarity * energy_weight
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    target_valence = user_prefs.get("valence")
    if target_valence is not None and song.get("valence") is not None:
        valence_similarity = max(0.0, 1 - abs(song["valence"] - target_valence))
        valence_points = valence_similarity * valence_weight
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    acousticness = song.get("acousticness")
    if likes_acoustic is not None and acousticness is not None:
        acoustic_match = acousticness >= 0.6 if likes_acoustic else acousticness < 0.6
        if acoustic_match:
            score += acoustic_bonus
            reasons.append(f"acoustic preference match (+{acoustic_bonus:.1f})")

    if not reasons:
        reasons.append("baseline similarity only")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank them highest-first, and return the top k."""
    scored_recommendations: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_recommendations.append((song, score, explanation))

    ranked_recommendations = sorted(
        scored_recommendations,
        key=lambda recommendation: recommendation[1],
        reverse=True,
    )
    return ranked_recommendations[:k]
