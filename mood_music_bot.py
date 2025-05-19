import streamlit as st
from transformers import pipeline
import base64

@st.cache_resource
def load_classifier():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=1
    )

classifier = load_classifier()


# Эмоции и соответствующие плейлисты
emotion_to_playlist = {
    "joy": {
        "name": "Happy Hits",
        "url": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
    },
    "sadness": {
        "name": "Life Sucks",
        "url": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"
    },
    "anger": {
        "name": "Rock Hard",
        "url": "https://open.spotify.com/playlist/37i9dQZF1DWXNFSTtym834"
    },
    "fear": {
        "name": "Chill Vibes",
        "url": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6"
    },
    "surprise": {
        "name": "New Music Friday",
        "url": "https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk"
    },
    "neutral": {
        "name": "Lofi study",
        "url": "https://open.spotify.com/playlist/10M75TUt3X1qbBhpuEw6el"
    }
}

# Установка фонового изображения
def set_background(image_path="img.jpg"):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Получение эмоции
def get_emotion(text):
    results = classifier(text)
    result = results[0][0]
    label = result['label'].lower()
    score = result['score']
    return label, score

# Получение плейлиста по эмоции
def get_playlist(emotion):
    playlist = emotion_to_playlist.get(emotion)
    if playlist:
        return playlist["name"], playlist["url"]
    else:
        return "Playlist not found", "#"

# Интерфейс
set_background("img.jpg")  # помести файл img.jpg рядом со скриптом

st.markdown("<h1 style='background-color: rgba(0, 0, 0, 0.7); padding: 1rem; border-radius: 10px; color: white; text-align: center; font-size: 40px; margin-top: 40px;'>🎧 MoodMusic AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='background-color: rgba(0, 0, 0, 0.7); padding: 1rem; border-radius: 10px; color: white; text-align: center;'>Tell me how you feel and I'll pick out some music for you.</p>", unsafe_allow_html=True)

user_input = st.text_input("Enter your mood:")

if user_input:
    emotion, confidence = get_emotion(user_input)
    playlist_name, playlist_url = get_playlist(emotion)

    st.markdown(f"🧠 **Emotion:** `{emotion}` (confidence: {confidence:.2f})")
    if playlist_url != "#":
        st.markdown(f"🎵 **Recommended playlist:** [{playlist_name}]({playlist_url})")
    else:
        st.markdown("⚠️ Unfortunately, no suitable playlist was found.")
