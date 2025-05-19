import streamlit as st
from transformers import pipeline
import base64

# Кешируем модель
@st.cache_resource
def load_classifier():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=1
    )

classifier = load_classifier()

# Эмоции и плейлисты
emotion_to_playlist = {
    "joy": {"name": "Happy Hits", "url": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"},
    "sadness": {"name": "Life Sucks", "url": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"},
    "anger": {"name": "Rock Hard", "url": "https://open.spotify.com/playlist/37i9dQZF1DWXNFSTtym834"},
    "fear": {"name": "Chill Vibes", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6"},
    "surprise": {"name": "New Music Friday", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk"},
    "neutral": {"name": "Lofi study", "url": "https://open.spotify.com/playlist/10M75TUt3X1qbBhpuEw6el"},
}

# Фон
def set_background(image_path="img.jpg"):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Фоновое изображение 'img.jpg' не найдено.")

# Стилизация заголовка и подзаголовка, инпута и результата
st.markdown("""
    <style>
    h1 {
        background-color: black;
        color: white;
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        font-size: 3rem;
        margin-top: 40px;
        margin-bottom: 0.5rem;
    }

    p.description {
        background-color: black;
        color: white;
        text-align: center;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        font-size: 1.2rem;
        margin-top: 5px;
        margin-bottom: 2rem;
    }

    input[type="text"] {
        background-color: black !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid white !important;
        padding: 0.5rem !important;
    }

    ::placeholder {
        color: #aaa !important;
    }
    </style>
""", unsafe_allow_html=True)

set_background("img.jpg")

# Заголовок и подзаголовок
st.markdown("<h1>🎧 MoodMusic AI</h1>", unsafe_allow_html=True)
st.markdown('<p class="description">Tell me how you feel and I\'ll pick out some music for you.</p>', unsafe_allow_html=True)

# Поле ввода
user_input = st.text_input("Enter your mood:")

if user_input:
    results = classifier(user_input)
    result = results[0][0]
    emotion = result['label'].lower()
    confidence = result['score']
    playlist = emotion_to_playlist.get(emotion, {"name": "Unknown", "url": "#"})

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
            🧠 <strong>Emotion detected:</strong> <code style='color: #1DB954; font-size: 20px;'>{emotion}</code><br><br>
            🔍 <strong>Confidence:</strong> {confidence:.2f}
        </div>
    """, unsafe_allow_html=True)

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
            <a href="{playlist['url']}" style="color: #1DB954; font-size: 20px; font-weight: bold;" target="_blank">
                {playlist['name']}
            </a>
        </div>
    """, unsafe_allow_html=True)
