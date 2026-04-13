"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list[dict], k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n=== {profile_name} ===")
    print(f"Preferences: {user_prefs}\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.82,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "focused",
            "energy": 0.38,
            "valence": 0.58,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "valence": 0.45,
            "likes_acoustic": False,
        },
        "Adversarial Sad Runner": {
            "genre": "pop",
            "mood": "melancholy",
            "energy": 0.9,
            "valence": 0.25,
            "likes_acoustic": False,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print_recommendations(profile_name, user_prefs, songs)

    experimental_profile = {
        **profiles["High-Energy Pop"],
        "genre_weight": 1.0,
        "energy_weight": 2.0,
    }
    print_recommendations("Experiment: High-Energy Pop with lower genre and higher energy weight", experimental_profile, songs)


if __name__ == "__main__":
    main()
