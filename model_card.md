# Music Recommender Model Card

## 1. Model Name

VibeFinder CLI

---

## 2. Intended Use

This recommender suggests a short ranked list of songs from a small classroom dataset. It is designed for learning how a content-based recommender works, not for real users in production. The model assumes that a user's taste can be summarized with a few preferences such as favorite genre, favorite mood, target energy, target valence, and whether they like acoustic sound.

---

## 3. How the Model Works

The model compares each song to one user profile and gives it points for matching features. Genre match is worth the most, mood match is worth less, and then the system adds similarity points based on how close the song is to the user's target energy and valence. It also gives a small bonus when the song's acousticness agrees with the user's acoustic preference. After every song gets a score, the list is sorted from highest to lowest and the top songs are returned with a plain-language explanation of why they scored well.

---

## 4. Data

The catalog has 18 songs in `data/songs.csv`. I expanded the starter dataset by adding songs from genres like house, hip hop, classical, country, blues, dream pop, world, and chiptune, along with moods like melancholy, calm, confident, nostalgic, and playful. The dataset covers a wider range than the original starter file, but it is still tiny and still misses a lot of real listening contexts such as multilingual music, lyrical themes, and live or instrumental variations.

---

## 5. Strengths

The system works best when the user profile lines up with a clear vibe already present in the dataset. For example, the chill lofi profile strongly favored `Focus Flow`, `Library Rain`, and `Midnight Coding`, which matches my intuition because all three share low energy and more acoustic texture. The intense rock profile also behaved well because `Storm Runner` clearly matched both the category labels and the numeric feel of that profile.

---

## 6. Limitations and Bias

One weakness I discovered is that the model can over-reward genre and high energy even when the mood is conflicting. In the adversarial profile with `genre="pop"`, `mood="melancholy"`, and `energy=0.9`, the system still ranked `Gym Hero` first because the pop match and strong energy similarity outweighed the emotional mismatch. This creates a small filter-bubble effect where users who like one genre keep seeing that genre even when another song matches the requested mood better. The dataset is also too small to represent many users fairly, so underrepresented genres and moods have fewer chances to appear in the top results.

---

## 7. Evaluation

I tested the system with four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial Sad Runner profile with conflicting preferences. I looked at whether the top five songs felt musically reasonable and whether the reasons list matched the scoring logic in `recommender.py`. The strongest result was that each normal profile produced a different top song: `Sunrise City` for pop, `Focus Flow` for lofi, and `Storm Runner` for rock. The most surprising result was the adversarial case, where `Gym Hero` still beat `Blue Hour Train`, showing that the current weights make genre and energy more powerful than mood in some situations.

I also ran one data experiment by lowering the genre weight from `2.0` to `1.0` and doubling the energy weight from `1.0` to `2.0` for the High-Energy Pop profile. After that change, `Rooftop Lights` moved above `Gym Hero`, which made the recommendations more varied but also less strict about genre. That experiment showed me that the system is sensitive to weight choices: changing one number does not just alter the score, it changes what the model thinks the user cares about most.

---

## 8. Future Work

I would improve the model by adding more user preferences and a better way to balance diversity in the top results. Right now the system only chases the nearest matches, so it can recommend songs that feel repetitive. I would also like to add artist diversity, a penalty for repeating the same genre too often, and a stronger way to represent emotional conflict so a "sad but energetic" user does not automatically get cheerful gym music.

---

## 9. Personal Reflection

Building this made it much clearer that recommendation systems are really collections of design choices hidden inside math. Even a simple score can feel smart when it matches a profile well, but it can also fail in very human ways when the weights do not reflect what the user actually meant. The project also made me think more carefully about real music apps, because when a song keeps showing up, it may not be because it is objectively best. It may just be that the system is over-trusting one signal.
