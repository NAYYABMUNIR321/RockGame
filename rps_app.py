# rps_app_sidebar.py
import streamlit as st
from PIL import Image
import random
import pandas as pd

st.set_page_config(page_title="Rock Paper Scissors", page_icon="🎮")

# --- CSS Styling ---
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 16px;
    margin: 5px;
}
.stButton>button:hover {
    background-color: #45a049;
}
.card {
    border: 2px solid #2196F3;
    border-radius: 10px;
    padding: 10px;
    background-color: #f0f8ff;
    margin-bottom: 10px;
    text-align:center;
}
.result-win {color:green; font-weight:bold; text-align:center;}
.result-lose {color:red; font-weight:bold; text-align:center;}
.result-draw {color:gray; font-weight:bold; text-align:center;}
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Settings ---
st.sidebar.title("🎮 Game Settings")

# Number of rounds
rounds_to_play = st.sidebar.slider(
    "Select number of rounds:",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

# Image size
img_size = st.sidebar.slider(
    "Adjust image size:",
    min_value=100,
    max_value=300,
    value=150,
    step=10
)

# Email & GitHub in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <p style='font-size:14px;'>
    Made by <strong>Nayab Munir</strong><br>
    Email: <a href='mailto:nayabhan84321@gmail.com'>nayabhan84321@gmail.com</a><br>
    GitHub: <a href='https://github.com/NAYYABMUNIR321' target='_blank'>@NAYYABMUNIR321</a>
    </p>
    """,
    unsafe_allow_html=True
)

# --- Load images safely and resize ---
def load_image(path, size=(img_size,img_size)):
    try:
        img = Image.open(path)
        img = img.resize(size)
        return img
    except Exception as e:
        st.error(f"Image not found: {path}")
        return None

imgs = {
    "Rock": load_image("images/rock.png"),
    "Paper": load_image("images/paper.png"),
    "Scissors": load_image("images/scissors.png")
}

# --- Title and player name ---
st.title("🎮 Rock — Paper — Scissors")
player_name = st.text_input("Enter your name:", value="Player").strip()
if player_name == "":
    player_name = "Player"

# --- Initialize session state ---
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "round" not in st.session_state:
    st.session_state.round = 0

# --- Choices ---
choices = ["Rock", "Paper", "Scissors"]
st.write("Choose your move (click the button under the image):")

# --- Show images with buttons ---
col1, col2, col3 = st.columns(3)
user_choice = None

with col1:
    if imgs["Rock"]:
        st.image(imgs["Rock"], caption="Rock", width=img_size)
    if st.button("Rock", key="btn_rock"):
        user_choice = "Rock"

with col2:
    if imgs["Paper"]:
        st.image(imgs["Paper"], caption="Paper", width=img_size)
    if st.button("Paper", key="btn_paper"):
        user_choice = "Paper"

with col3:
    if imgs["Scissors"]:
        st.image(imgs["Scissors"], caption="Scissors", width=img_size)
    if st.button("Scissors", key="btn_scissors"):
        user_choice = "Scissors"

# --- Play round if choice made ---
if user_choice:
    comp_choice = random.choice(choices)
    st.session_state.round += 1

    # Determine result
    if user_choice == comp_choice:
        result_text = "Draw"
        result_class = "result-draw"
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissors" and comp_choice == "Paper"):
        result_text = "You Win"
        result_class = "result-win"
        st.session_state.user_score += 1
    else:
        result_text = "Computer Wins"
        result_class = "result-lose"
        st.session_state.computer_score += 1

    # Save history
    st.session_state.history.append({
        "Round": st.session_state.round,
        "Player": user_choice,
        "Computer": comp_choice,
        "Result": result_text
    })

    # Show round result
    st.markdown("---")
    rcol1, rcol2, rcol3 = st.columns(3)
    with rcol1:
        st.subheader(f"{player_name}'s Move")
        if imgs[user_choice]:
            st.image(imgs[user_choice], width=img_size)
        st.write(user_choice)
    with rcol2:
        st.markdown(f'<p class="{result_class}">{result_text if result_text!="Draw" else "It\'s a Draw!"}</p>', unsafe_allow_html=True)
    with rcol3:
        st.subheader("Computer's Move")
        if imgs[comp_choice]:
            st.image(imgs[comp_choice], width=img_size)
        st.write(comp_choice)

# --- Scoreboard ---
st.markdown("## Scoreboard")
st.markdown(f'<div class="card"><p>{player_name} Score: {st.session_state.user_score}</p>'
            f'<p>Computer Score: {st.session_state.computer_score}</p></div>', unsafe_allow_html=True)

# --- History table ---
st.markdown("## History")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.table(df.sort_values("Round", ascending=False).reset_index(drop=True))
else:
    st.write("No rounds played yet. Play a round to see history!")

# --- Controls ---
reset_col1, reset_col2 = st.columns(2)
with reset_col1:
    if st.button("Reset Scores & History"):
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.history = []
        st.session_state.round = 0

with reset_col2:
    if st.button("Next Round (clear last display)"):
        pass  # auto-refresh handles display
