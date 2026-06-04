import streamlit as st
import math
import time
import base64

st.set_page_config(page_title="AI Tic Tac Toe", layout="wide")

# ----- Session State -----
if 'show_game' not in st.session_state:
    st.session_state.show_game = False
if 'board' not in st.session_state:
    st.session_state.board = [' '] * 9
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = "Your turn (❌)"
if 'score' not in st.session_state:
    st.session_state.score = {"You": 0, "AI": 0, "Tie": 0}
if 'pending_ai' not in st.session_state:
    st.session_state.pending_ai = False

# ----- Fullscreen Background Image -----
def set_image_background(image_path):
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    h1, h3, p {{
        color: white !important;
        text-align: center;
        text-shadow: 2px 2px 6px black;
    }}
    .block-container {{
        padding-top: 4rem;
        padding-bottom: 4rem;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ----- Gradient Background for Game -----
def set_game_background():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #b6fbff, #83a4d4);
    }
    h1, h3, p, .caption, .stCaption {
        color: #222222 !important;
        text-shadow: 1px 1px 2px #ffffff;
    }
    button[kind="secondary"] {
        font-size: 32px !important;
        height: 100px !important;
        background-color: white !important;
        color: black !important;
        border-radius: 15px !important;
        border: 2px solid #444 !important;
        font-weight: bold;
    }
    .block-container {
        padding: 2rem;
        border-radius: 15px;
    }
    .score-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 10px 15px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        margin-top: 10px;
        margin-bottom: 10px;
        text-align: center;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    .score-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ----- Game Logic -----
def print_board_ui():
    rows = [st.columns(3) for _ in range(3)]
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            cell = st.session_state.board[idx]
            with rows[i][j]:
                if cell == ' ' and not st.session_state.game_over:
                    if st.button(" ", key=idx, use_container_width=True):
                        human_move(idx)
                else:
                    st.button(cell, key=idx, use_container_width=True, disabled=True)

def winner(board, player):
    combos = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(board[i] == player for i in combo) for combo in combos)

def is_full(board):
    return ' ' not in board

def minimax(board, is_maximizing):
    if winner(board, 'O'): return 1
    if winner(board, 'X'): return -1
    if is_full(board): return 0
    best = -math.inf if is_maximizing else math.inf
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O' if is_maximizing else 'X'
            score = minimax(board, not is_maximizing)
            board[i] = ' '
            best = max(score, best) if is_maximizing else min(score, best)
    return best

def ai_move():
    st.session_state.message = "🤖 AI is thinking..."
    with st.spinner("AI move..."):
        time.sleep(1.0)
    best_score = -math.inf
    move = None
    for i in range(9):
        if st.session_state.board[i] == ' ':
            st.session_state.board[i] = 'O'
            score = minimax(st.session_state.board, False)
            st.session_state.board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    if move is not None:
        st.session_state.board[move] = 'O'

def human_move(pos):
    if st.session_state.board[pos] == ' ' and not st.session_state.game_over:
        st.session_state.board[pos] = 'X'
        if winner(st.session_state.board, 'X'):
            st.session_state.message = "🎉 You win!"
            st.session_state.score["You"] += 1
            st.session_state.game_over = True
        elif is_full(st.session_state.board):
            st.session_state.message = "😐 It's a tie!"
            st.session_state.score["Tie"] += 1
            st.session_state.game_over = True
        else:
            st.session_state.pending_ai = True

# ----- Screens -----
def start_screen():
    set_image_background("assets/game.jpg")
    st.markdown("<h1>🎮 AI Tic Tac Toe</h1>", unsafe_allow_html=True)
    st.markdown("<p>Play against an unbeatable AI (Minimax Algorithm)</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶ Start Game"):
        st.session_state.show_game = True

def game_screen():
    set_game_background()
    st.markdown("<h1>🤖 AI-Based Tic Tac Toe</h1>", unsafe_allow_html=True)
    st.markdown("<p><b>You = ❌ | AI = ⭕</b></p>", unsafe_allow_html=True)

    # 👾 AI move if scheduled
    if st.session_state.pending_ai and not st.session_state.game_over:
        ai_move()
        st.session_state.pending_ai = False
        if winner(st.session_state.board, 'O'):
            st.session_state.message = "😈 AI wins!"
            st.session_state.score["AI"] += 1
            st.session_state.game_over = True
        elif is_full(st.session_state.board):
            st.session_state.message = "😐 It's a tie!"
            st.session_state.score["Tie"] += 1
            st.session_state.game_over = True

    print_board_ui()
    st.markdown(f"<h3>{st.session_state.message}</h3>", unsafe_allow_html=True)

    # 🎨 Styled Scoreboard Box (smaller now)
    st.markdown("""
    <div class="score-box">
        <div class="score-title">📊 Scoreboard</div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("You", st.session_state.score["You"])
    col2.metric("AI", st.session_state.score["AI"])
    col3.metric("Tie", st.session_state.score["Tie"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Restart Game"):
        st.session_state.board = [' '] * 9
        st.session_state.game_over = False
        st.session_state.message = "Your turn (❌)"
        st.session_state.pending_ai = False

# ----- Main -----
if st.session_state.show_game:
    game_screen()
else:
    start_screen()
