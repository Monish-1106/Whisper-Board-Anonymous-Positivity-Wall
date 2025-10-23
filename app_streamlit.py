import streamlit as st
import json
import random
import os
from datetime import datetime
from whisper_core import load_posts, save_post, delete_post
from dotenv import load_dotenv

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # fallback default

# ==========================
# App Configuration
# ==========================
st.set_page_config(page_title="WhisperBoard 💬", layout="wide")

st.markdown("""
<style>
    .stTextInput>div>div>input {
        background-color: #1e1e1e;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# Sidebar: Admin Section
# ==========================
st.sidebar.header("🔐 Admin Login")

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

admin_input = st.sidebar.text_input("Enter admin password:", type="password")

if admin_input:
    if admin_input == ADMIN_PASSWORD:
        st.sidebar.success("Welcome, Admin!")
        st.session_state.is_admin = True
    else:
        st.sidebar.error("Incorrect password.")

# ==========================
# Helper: Load Bad Words
# ==========================
def load_bad_words():
    if os.path.exists("bad_words.txt"):
        with open("bad_words.txt", "r") as f:
            return [w.strip().lower() for w in f.readlines()]
    return []

bad_words = load_bad_words()

def contains_bad_words(text):
    for word in bad_words:
        if word in text.lower():
            return True
    return False

# ==========================
# Post a Whisper Section
# ==========================
st.title("💌 WhisperBoard")
st.write("Share an uplifting message anonymously and brighten someone’s day 💖")

st.subheader("📝 Post a Whisper")

# CAPTCHA stays stable until reset
if "captcha_a" not in st.session_state or "captcha_b" not in st.session_state:
    st.session_state.captcha_a = random.randint(1, 9)
    st.session_state.captcha_b = random.randint(1, 9)

message = st.text_area("Your positive message:", height=150)

# Display CAPTCHA
st.write(f"What is {st.session_state.captcha_a} + {st.session_state.captcha_b}? (Prove you're human)")
user_answer = st.text_input("Your answer here:")

# Handle submission
if st.button("Submit Whisper"):
    if not message.strip():
        st.warning("Please write a message before submitting.")
    elif contains_bad_words(message):
        st.error("Please avoid using inappropriate words.")
    else:
        try:
            ans = int(user_answer.strip())
            correct = st.session_state.captcha_a + st.session_state.captcha_b
            if ans == correct:
                save_post(message)
                st.success("✨ Whisper added successfully!")

                # Reset CAPTCHA
                st.session_state.captcha_a = random.randint(1, 9)
                st.session_state.captcha_b = random.randint(1, 9)
            else:
                st.error("❌ CAPTCHA failed. Try again.")
                # Reset CAPTCHA for a new question
                st.session_state.captcha_a = random.randint(1, 9)
                st.session_state.captcha_b = random.randint(1, 9)
        except ValueError:
            st.error("Please enter a number for the CAPTCHA.")

# ==========================
# Display Whispers
# ==========================
st.subheader("🌈 Community Whispers")

posts = load_posts()
if posts:
    for post in reversed(posts):
        st.markdown(f"💬 *{post['message']}*  \n🕒 _{post['timestamp']}_")
        st.divider()
else:
    st.info("No whispers yet. Be the first to share positivity! 🌟")

# ==========================
# Admin Controls
# ==========================
if st.session_state.is_admin:
    st.sidebar.subheader("🗑️ Manage Whispers")
    posts = load_posts()
    if posts:
        for i, post in enumerate(reversed(posts)):
            if st.sidebar.button(f"Delete: {post['message'][:20]}..."):
                delete_post(len(posts) - 1 - i)
                st.sidebar.success("Post deleted!")
                st.rerun()
    else:
        st.sidebar.info("No posts to manage.")


