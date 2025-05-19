import streamlit as st
from transformers import pipeline
import base64

# Настройки страницы
st.set_page_config(page_title="MoodMusic AI", page_icon="🎧", layout="centered")

# Подключаем модель и кэшируем
@st.cache_resource
def load_classifier():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=1
    )

classifier = load_classifier()

# Сопоставление эмоций и плейлистов
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

# 🔳 Установка фонового изображения
def set_background(image_path="img.jpg"):
    try:
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
    except FileNotFoundError:
        st.warning("⚠️ Фоновое изображение 'img.jpg' не найдено.")

# 🧠 Анализ текста на эмоции
def get_emotion(text):
    results = classifier(text)
    result = results[0][0]
    label = result['label'].lower()
    score = result['score']
    return label, score

# 🎧 Получение подходящего плейлиста
def get_playlist(emotion):
    playlist = emotion_to_playlist.get(emotion)
    if playlist:
        return playlist["name"], playlist["url"]
    else:
        return "Playlist not found", "#"

# Установка фона
set_background("img.jpg")  # Помести изображение рядом со скриптом

# 🎨 Пользовательский CSS (тёмный брутализм)
st.markdown("""
    <style>
        * {
            font-family: 'Courier New', monospace;
        }
        .title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: white;
            margin-bottom: 10px;
            padding: 0.5rem;
            background-color: rgba(0, 0, 0, 0.7);
            border: 3px solid white;
            border-radius: 12px;
        }
        .subtitle {
            text-align: center;
            color: #ccc;
            padding: 0.5rem;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .result-box {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 1rem;
            border: 2px dashed white;
            border-radius: 10px;
            margin-top: 1.5rem;
        }
        .playlist-link {
            font-size: 1.2rem;
            font-weight: bold;
            color: #00ffcc;
        }
    </style>
""", unsafe_allow_html=True)

# 🧾 Интерфейс
st.markdown('<div class="title">🎧 MoodMusic AI</div>', unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Tell me how you feel and I'll pick out some music for you.</div>", unsafe_allow_html=True)

user_input = st.text_input("💬 Enter your mood text:")

if user_input:
    emotion, confidence = get_emotion(user_input)
    playlist_name, playlist_url = get_playlist(emotion)

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.markdown(f"🧠 <strong>Detected emotion:</strong> <code>{emotion}</code>", unsafe_allow_html=True)
    st.markdown(f"🔎 <strong>Confidence:</strong> <code>{confidence:.2f}</code>", unsafe_allow_html=True)

    if playlist_url != "#":
        st.markdown(f"🎵 <strong>Recommended playlist:</strong> <a class='playlist-link' href='{playlist_url}' target='_blank'>{playlist_name}</a>", unsafe_allow_html=True)
    else:
        st.markdown("⚠️ Unfortunately, no suitable playlist was found.")

    st.markdown("</div>", unsafe_allow_html=True)
