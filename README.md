# Tic-Tac-Toe Game with Django

A simple implementation of the Tic-Tac-Toe game built with Django. This project allows two users to play against each other, with game state, moves, and winner tracking handled on the server side.

---

## 🚀 Features
- **User Authentication**: Players can log in and start a game.
- **Game State**: The game board is saved in the database, with real-time updates for each move.
- **Turn-Based Gameplay**: Enforces alternate turns between players.
- **Winner/Draw Detection**: Automatically checks for a winner or declares a draw if the board is full.
- **Responsive UI**: Playable on both desktop and mobile browsers.

---

## 🛠 Tech Stack
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript (AJAX)
- **Database**: SQLite (default) or PostgreSQL
- **Web Server**: Django's development server

---

## ⚙️ Setup Instructions

### Prerequisites
Make sure you have the following installed:
- **Python 3.8+**
- **Django 4.x**
- **psycopg2** (if using PostgreSQL)

### 1. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
