# VibeFinder 1.0

## Model Name

VibeFinder 1.0

## Goal / Task

This system suggests songs from a small catalog. It tries to predict which songs best match one user's vibe.

## Data Used

The dataset has 18 songs in `data/songs.csv`. Each song includes `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The dataset is small, so it cannot represent all music styles or all kinds of listeners.

## Algorithm Summary

Each song gets points for matching the user's preferences. A genre match adds the most points. A mood match adds fewer points. Then the system adds similarity points when the song's energy and valence are close to the user's target values. It also gives a small bonus when the song's acousticness matches the user's acoustic preference. After that, it sorts all songs by score and returns the top results.

## Observed Behavior / Biases

The system works well when the user wants a clear vibe that already exists in the dataset. It matched `Focus Flow` to a chill lofi profile and `Storm Runner` to an intense rock profile, which felt right. One weakness is that genre and energy can overpower mood. In the adversarial profile with `genre="pop"` and `mood="melancholy"`, `Gym Hero` still ranked first even though it does not feel sad. This shows a small filter-bubble problem.

## Evaluation Process

I tested High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial Sad Runner profile. I checked whether the top songs felt reasonable and whether the printed reasons matched the scoring logic. I also ran one experiment where I lowered the genre weight and doubled the energy weight. That changed the ranking and showed that the recommender is very sensitive to its weights.

## Intended Use and Non-Intended Use

This system is intended for classroom learning and simple experiments with recommendation logic. It is not meant for real users, music discovery at scale, or any high-stakes decision. It should not be treated as a complete or fair model of a person's music taste.

## Ideas for Improvement

- Add more songs and more genres so the catalog is less biased.
- Add diversity rules so the top results are not all from the same style.
- Add more user features, like favorite tempo range or dislike of repeated artists.

## Personal Reflection

My biggest learning moment was seeing how one small weight change can completely change what the model seems to care about. Using AI tools helped me move faster when I was drafting logic, testing profiles, and checking explanations, but I still had to verify the results myself because the suggestions were only useful if they matched the real code and outputs. I was surprised that such a simple point system could still feel like a recommendation engine when the profile and dataset lined up well. If I extended this project, I would try a diversity rule next so the recommender would feel less repetitive.
