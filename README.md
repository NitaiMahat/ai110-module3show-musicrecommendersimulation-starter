# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version of the simulator recommends songs by comparing each track's genre, mood, energy, valence, and acousticness to a user's taste profile. It prioritizes matching the user's stated vibe first, then uses numeric features to reward songs that are closest to the user's preferred feel instead of simply favoring songs with the biggest values.

---

## How The System Works

Real-world recommenders combine item features and user preferences, then rank the items with the strongest fit. My version does the same thing in a much simpler and more transparent way: it looks at the vibe features attached to each song, compares them to one user taste profile, gives each song a score, and returns the top `k` results. In my experience, musical vibe is mostly defined by a mix of category labels and feel-based numbers, so I want `genre` and `mood` to anchor the recommendation while `energy`, `valence`, and `acousticness` fine-tune it.

After reviewing `data/songs.csv`, the strongest features for a simple content-based system are `genre`, `mood`, `energy`, `valence`, and `acousticness`. The dataset already includes two helpful numeric depth features, `danceability` and `acousticness`, so I kept those and expanded the catalog with more genres and moods such as `hip hop`, `house`, `classical`, `country`, `world`, `blues`, `dream pop`, `playful`, `confident`, `calm`, and `nostalgic`. These additions make it easier for the system to tell the difference between very different vibes instead of only choosing among pop, lofi, and rock.

My user profile is:

```python
user_prefs = {
    "genre": "lofi",
    "mood": "focused",
    "energy": 0.38,
    "valence": 0.58,
    "likes_acoustic": True,
}
```

I think this profile is broad enough to separate "intense rock" from "chill lofi" because it combines a categorical preference (`genre`, `mood`) with low target energy and a preference for acoustic texture. If the profile only used one feature, like genre alone, the system would be too narrow and miss songs that match the same overall feel in neighboring styles.

My finalized Algorithm Recipe is:

- `+2.0` points for a `genre` match because genre is the strongest high-level signal.
- `+1.0` point for a `mood` match because mood matters a lot but is slightly less specific than genre.
- Add an `energy` similarity score using `1 - abs(song_energy - user_energy)` so closer songs earn more points.
- Add a smaller `valence` similarity score using `1 - abs(song_valence - user_valence)` to capture emotional brightness.
- Add `+0.5` points when the song's `acousticness` agrees with whether the user likes acoustic sound.

This system needs both a scoring rule and a ranking rule. The scoring rule judges one song at a time and turns its features into a number. The ranking rule sorts the full list of song scores from highest to lowest and returns the top recommendations.

The `Song` object in my simulation uses: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

The `UserProfile` object stores: `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`.

```mermaid
flowchart LR
    A[User Preferences] --> B[Loop Through Each Song in songs.csv]
    B --> C[Check Genre and Mood Matches]
    C --> D[Compute Energy and Valence Similarity]
    D --> E[Add Acoustic Preference Bonus]
    E --> F[Assign Total Score to Song]
    F --> G[Sort All Songs by Score]
    G --> H[Return Top K Recommendations]
```

One bias I expect is that this system may over-prioritize `genre` and push down songs from other genres that still match the same mood and energy. It also depends on human-written labels in a tiny dataset, so if those labels are inconsistent, the recommender will inherit that bias.

CLI output snapshot from `python -m src.main` with the default `pop/happy` profile:

```text
Loaded songs: 18

Top recommendations:

1. Sunrise City by Neon Echo
   Score: 5.46
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.98), valence similarity (+0.98), acoustic preference match (+0.5)

2. Gym Hero by Max Pulse
   Score: 4.32
   Reasons: genre match (+2.0), energy similarity (+0.87), valence similarity (+0.95), acoustic preference match (+0.5)

3. Rooftop Lights by Indigo Parade
   Score: 3.45
   Reasons: mood match (+1.0), energy similarity (+0.96), valence similarity (+0.99), acoustic preference match (+0.5)
```

Evaluation snapshots from `python -m src.main` with multiple profiles:

```text
=== Chill Lofi ===
1. Focus Flow by LoRoom
   Score: 5.47
2. Library Rain by Paper Lanterns
   Score: 4.45
3. Midnight Coding by LoRoom
   Score: 4.44

=== Deep Intense Rock ===
1. Storm Runner by Voltline
   Score: 5.46
2. Gym Hero by Max Pulse
   Score: 3.17
3. Night Drive Loop by Neon Echo
   Score: 2.29

=== Adversarial Sad Runner ===
1. Gym Hero by Max Pulse
   Score: 3.95
2. Sunrise City by Neon Echo
   Score: 3.83
3. Blue Hour Train by Ash Harbor
   Score: 2.40
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

I tested four profiles in the CLI: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial profile with conflicting preferences (`genre="pop"`, `mood="melancholy"`, `energy=0.9`). The normal profiles behaved the way I expected: each one found a different top song that matched the intended vibe. The adversarial profile was more revealing because `Gym Hero` still ranked first, which showed me that genre and energy can overpower mood in the current design.

I also ran a small weight-shift experiment. I reduced the genre bonus from `+2.0` to `+1.0` and doubled the energy weight from `1.0` to `2.0` for the High-Energy Pop profile. After that change, `Rooftop Lights` moved above `Gym Hero`, which made the results more varied but also less strict about genre. That made the recommendations feel different rather than simply more accurate.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project made it clear that recommenders are really a chain of small design choices. The system feels convincing when the profile is clear and the dataset contains a close match, but it can produce odd results when the weights do not reflect the user's real intent. Seeing `Gym Hero` show up for an emotionally mixed profile helped me understand how easily one strong signal can dominate the rest.

I also learned that bias in a recommender does not have to look dramatic to matter. A small genre bonus or a tiny catalog can quietly create a filter bubble, where the same kinds of songs keep rising to the top even when another part of the profile points somewhere else. That is a useful reminder that transparency and human judgment still matter, even in a simple classroom system.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

