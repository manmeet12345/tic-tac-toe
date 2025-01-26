def make_move(game, position, symbol):
    """
    Update the game board for a given move.

    Args:
        game (Game): The Game object representing the current game.
        position (int): The position (0-8) on the board where the move is to be made.
        symbol (str): The symbol ('X' or 'O') to place on the board.

    Returns:
        bool: True if the move was successfully made, False otherwise.
    """
    board = game.board

    # Ensure the position is valid and empty
    if board[position] == " ":
        board[position] = symbol  # Make the move
        game.board = board  # Update the game board
        game.save()  # Save changes to the database
        return True

    return False  # Move was invalid

def check_winner(board):
    """
    Check if there is a winner on the board.

    Args:
        board (list): A list representing the game board.

    Returns:
        str: 'X', 'O', or None if there is no winner.
    """
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6],             # Diagonal
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != " ":
            return board[combo[0]]  # Return the winner ('X' or 'O')

    return None  # No winner

def is_draw(board):
    """
    Check if the game is a draw (no empty spaces left).

    Args:
        board (list): A list representing the game board.

    Returns:
        bool: True if the game is a draw, False otherwise.
    """
    return all(cell != " " for cell in board)