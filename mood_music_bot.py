import streamlit as st
from transformers import pipeline
import base64

# Настройка страницы
st.set_page_config(page_title="MoodMusic AI", page_icon="🎧", layout="centered")

# Кешируем модель
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
    "joy": {"name": "Happy Hits", "url": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"},
    "sadness": {"name": "Life Sucks", "url": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"},
    "anger": {"name": "Rock Hard", "url": "https://open.spotify.com/playlist/37i9dQZF1DWXNFSTtym834"},
    "fear": {"name": "Chill Vibes", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6"},
    "surprise": {"name": "New Music Friday", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk"},
    "neutral": {"name": "Lofi study", "url": "https://open.spotify.com/playlist/10M75TUt3X1qbBhpuEw6el"}
}

# Установка фонового изображения
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
                z-index: 0;
                position: relative;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("⚠️ Фоновое изображение 'img.jpg' не найдено.")

# Получение эмоции
def get_emotion(text):
    results = classifier(text)
    result = results[0][0]
    label = result['label'].lower()
    score = result['score']
    return label, score

# Получение плейлиста
def get_playlist(emotion):
    playlist = emotion_to_playlist.get(emotion)
    if playlist:
        return playlist["name"], playlist["url"]
    return "Playlist not found", "#"

# Установка фона
set_background("img.jpg")

# Стилизация
st.markdown("""
    <style>
        * {
            color: white !important;
        }
        body {
            background-color: transparent;
        }
        .main-container {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 2rem;
            max-width: 700px;
            min-height: 90vh;
            margin: auto;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
        .title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #ccc;
            margin-bottom: 2rem;
        }
        .result {
            background-color: black;
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(255,255,255,0.1);
            font-size: 18px;
        }
        a {
            color: #00ffff;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Интерфейс
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="title">🎧 MoodMusic AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tell me how you feel and I\'ll pick a playlist for your mood.</div>', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Стили для input */
    div[data-baseweb="input"] > div {
        background-color: black !important;
        color: white !important;
        border: 1px solid white;
        border-radius: 10px;
    }

    /* Стили для текста внутри input */
    input {
        color: white !important;
        background-color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

user_input = st.text_input("💬 Введите ваше настроение:")

if user_input:
    emotion, confidence = get_emotion(user_input)
    playlist_name, playlist_url = get_playlist(emotion)

    st.markdown(f"""
    <div style="
        background-color: black;
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 0 15px rgba(255,255,255,0.1);
        font-size: 18px;
    ">
        🧠 <strong>Emotion detected:</strong> <code style='background-color: black; color: #1DB954; font-size: 20px;'>{emotion}</code><br><br>
        🔍 <strong>Confidence:</strong> {confidence:.2f}
    </div>
""", unsafe_allow_html=True)

if playlist_url != "#":
    st.markdown(f"""
        <div style="
            background-color: black;
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(255,255,255,0.1);
            font-size: 18px;
        ">
            🎵 <strong>Recommended playlist:</strong><br>
            <a href="{playlist_url}" style="color: #1DB954; font-size: 20px; font-weight: bold;" target="_blank">
                {playlist_name}
            </a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="
            background-color: black;
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(255,255,255,0.1);
            font-size: 18px;
        ">
            ⚠️ Unfortunately, no suitable playlist was found.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
