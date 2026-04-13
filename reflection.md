# Evaluation Reflections

## Profile Comparisons

High-Energy Pop vs Chill Lofi:
The outputs changed a lot in a way that made sense. The pop profile favored `Sunrise City` and `Gym Hero` because both songs are upbeat, bright, and non-acoustic, while the lofi profile moved toward `Focus Flow`, `Library Rain`, and `Midnight Coding` because those tracks are lower-energy and more acoustic.

High-Energy Pop vs Deep Intense Rock:
Both profiles liked energetic songs, but the rock profile shifted toward `Storm Runner` because it matched both `genre="rock"` and `mood="intense"`. This shows that energy alone is not deciding the results. The category labels still matter a lot when the user asks for a specific style.

Chill Lofi vs Deep Intense Rock:
These profiles produced nearly opposite outputs. The lofi profile preferred softer songs with acoustic texture and low energy, while the rock profile pulled in louder songs with higher energy and lower acousticness. That difference makes sense because the two users are asking for very different listening contexts.

Deep Intense Rock vs Adversarial Sad Runner:
This comparison exposed a weakness. Even though the adversarial profile asked for `melancholy`, the system still ranked `Gym Hero` highly because it is pop, high-energy, and non-acoustic. That tells me the current scoring logic can miss emotional nuance when one strong feature combination overwhelms the mood signal.

High-Energy Pop Baseline vs Weight-Shift Experiment:
When I lowered genre weight and doubled energy weight, `Rooftop Lights` moved above `Gym Hero`. That makes sense because `Rooftop Lights` is very close on energy and valence, even without a pop genre match. The experiment made the results more flexible, but it also made the system less loyal to the user's stated genre.
