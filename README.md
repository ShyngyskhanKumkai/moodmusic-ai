# moodmusic-ai
An AI-powered music recommendation app that detects your emotion from text and suggests a Spotify playlist.
1. Overview
MoodMusic AI is an intelligent system implemented as a web application that performs automatic sentiment analysis of user-provided text and recommends music that aligns with the detected emotional tone.

The project integrates modern Natural Language Processing (NLP) techniques with a recommendation mechanism, offering a user-friendly product that merges artificial intelligence with entertainment.

2. Objectives and Goals
Project Objectives:

To analyze free-form user text and classify it according to basic human emotions.

To suggest a music playlist that corresponds to the detected emotion.

To provide a fast, intuitive, and visually appealing interface.

Goals:

Employ a pre-trained NLP model for emotion classification.

Implement an interactive web interface.

Optimize performance through caching and lightweight styling.

3. Technology Stack
Technology	Purpose
Python 3.10+	Programming language
Streamlit	Web interface and UI rendering
Hugging Face Transformers	Pretrained NLP model provider
Model: j-hartmann/emotion-english-distilroberta-base	Emotion classification
CSS + Base64	Interface styling
Spotify	Source for curated playlists

4. Model Description
The core of the project is a fine-tuned transformer model called j-hartmann/emotion-english-distilroberta-base, available via the Hugging Face Model Hub. It is based on DistilRoBERTa, a distilled version of RoBERTa, trained specifically to classify short English texts into one of six emotional categories:

Joy

Sadness

Anger

Fear

Surprise

Neutral

The model returns the most likely emotion along with a confidence score, making it suitable for real-time sentiment classification in interactive applications.

5. System Workflow
The user enters a phrase expressing their thoughts or feelings.

The text is passed to the model for inference.

The model predicts the dominant emotion in the input.

A corresponding Spotify playlist is displayed based on the predicted emotion.

The user can click the playlist link to start listening immediately.

6. User Interface and Architecture
Developed using Streamlit to enable rapid web-based prototyping.

Styled with embedded CSS to follow a dark minimalist aesthetic.

A base64-encoded background image is used to eliminate external dependencies.

Caching mechanisms are employed to avoid reloading the model on every input.

Each of the six emotional categories is associated with a preselected Spotify playlist.

7. Usage Example
Input Text	Predicted Emotion	Recommended Playlist
I feel amazing today	joy	Energetic and uplifting music
Everything is terrible	sadness	Reflective or melancholic music
I'm so scared of what might happen	fear	Calming or supportive tracks

8. Future Enhancements
The application is designed to be scalable and may be extended in the following directions:

Multilingual support: Emotion recognition in various languages.

Voice input: Integration of speech recognition for hands-free interaction.

User personalization: Playlists adapted to individual taste through API integrations.

Emotion history tracking: Analysis of emotional patterns over time.

9. Project Structure
bash
Копировать
Редактировать
MoodMusicAI/
├── mood_music_bot.py          # Core application script
├── requirements.txt           # Dependencies list
├── README.md                  # Project documentation
├── background.png (optional)  # Background image (embedded)
10. Installation & Execution
Install dependencies:

bash
Копировать
Редактировать
pip install -r requirements.txt
Run the application:

bash
Копировать
Редактировать
streamlit run mood_music_bot.py
11. Author Information
Developer: [Kumkay Shynggyskhan]
Completion Date: [20.05.2025]
Contact: [Email / GitHub / LinkedIn]
