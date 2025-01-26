# Tic-Tac-Toe Game with Django

This project is a simple implementation of the Tic-Tac-Toe game built with Django. It allows two users to play against each other, with game state, moves, and winner tracking handled on the server side.

## Features
- **User Authentication**: Players can log in and start a game.
- **Game State**: The game board is saved in the database, and each player's move is reflected in real-time.
- **Turn-based Gameplay**: Players alternate turns. The game enforces the correct turn sequence.
- **Draw & Winner Detection**: The game checks for a winner after every move and declares a draw if all cells are filled with no winner.
- **Responsive UI**: The game can be played on both desktop and mobile browsers.

## Tech Stack
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript (AJAX)
- **Database**: SQLite (default) or PostgreSQL

## Setup Instructions

### 1. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure the Database
- **SQLite**: No additional configuration is required (default).
- **PostgreSQL**:
  ```bash
  pip install psycopg2
  ```
  Edit the `DATABASES` section in `settings.py` to set up PostgreSQL.

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

### 6. Run the Development Server
```bash
python manage.py runserver
```
The app will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## How to Play
1. Log in as a user (or create a new account).
2. Start a new game or join an existing one.
3. Click on the empty cells to make your move.
4. The game alternates turns between Player X and Player O.
5. The game ends when there is a winner or a draw.

## Game Logic

### Models
- **Game**: Contains details of the game, such as players, current turn, board state, and game status.
  - `board`: The board is stored as a list of 9 strings, representing the 9 cells. Each cell is either " ", "X", or "O".
  - `current_turn`: Tracks the player whose turn it is.
  - `winner`: Stores the winner of the game, if applicable.

### Views
- **`game_move`**: Handles the game logic of making a move. It checks if the move is valid, updates the board, checks for a winner, or a draw.
- **`game_status`**: Provides the current state of the game, including the board, turn, and status.

### Utility Functions
- **`make_move`**: Updates the board with the player's move and saves the game.
- **`check_winner`**: Checks the board for a winning combination.
- **`is_draw`**: Checks if the game is a draw (i.e., the board is full and there is no winner).
