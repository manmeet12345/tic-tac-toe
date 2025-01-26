from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_protect
import json
from django.http import JsonResponse
from . models import Game, Move
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import make_move, check_winner, is_draw


# Template Views

def home_view(request):
    context = {}
    
    return render(request, 'game/home.html', context)
    
@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
    
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')
        
        try:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Registration successful!')
            #return redirect('game')  # Redirect to game page after registration
            return render(request, 'login.html')
        
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            #return render(request, 'login.html')
            return redirect('login')
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('game_list')  # Redirect to game page after login
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    #redirect('register')
    return render(request, 'register.html')

@login_required
def game_list(request):
    """View for displaying list of user's games"""
    games = Game.objects.filter(
        Q(player1=request.user) | Q(player2=request.user)
    ).order_by('-updated_at')
    
    return render(request, 'game_list.html', {'games': games})

@login_required
@ensure_csrf_cookie
def start_game(request):
    """View for creating a new game"""
    print("1. View called")
    if request.method != 'POST':
        print("2. Not POST method")
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    try:
        print("3. Request body:", request.body)
        data = json.loads(request.body)
        opponent_username = data.get('opponent')
        print("4. Parsed data:", data)
        # Validate opponent exists
        try:
            opponent = User.objects.get(username=opponent_username)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Opponent not found'
            })

        # Check if opponent is not the same as current user
        if opponent == request.user:
            return JsonResponse({
                'success': False,
                'error': 'You cannot play against yourself'
            })

        # Check if there's already an active game between these players
        existing_game = Game.objects.filter(
            ((Q(player1=request.user) & Q(player2=opponent)) |
             (Q(player1=opponent) & Q(player2=request.user))) &
            Q(status='in_progress')
        ).first()

        if existing_game:
            return JsonResponse({
                'success': True,
                'redirect_url': f'/game/{existing_game.id}'
            })

        # Create new game
        game = Game.objects.create(
            player1=request.user,
            player2=opponent,
            status='in_progress',
            current_turn=request.user,  # First player starts
            board=[''] * 9  # Empty board
        )

        return JsonResponse({
            'success': True,
            'redirect_url': f'/game/{game.id}'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
    
    
@login_required
def new_game(request):
    """View for creating a new game"""
    if request.method == 'POST':
        opponent_username = request.POST.get('opponent')
        try:
            opponent = User.objects.get(username=opponent_username)
            
            if opponent == request.user:
                messages.error(request, 'You cannot play against yourself!')
                return redirect('new_game')
                
            game = Game.objects.create(
                player1=request.user,
                player2=opponent,
                board=[' '] * 9,
                current_turn=request.user
            )
            
            return redirect('game_board', game_id=game.id)
            
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')
            return redirect('new_game')
    
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'new_game.html',{'users': users})

@login_required
def game_board(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    board_positions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
    ]
    context = {
        'game': game,
        'board': list(game.board),
        'current_user': request.user,
        'range_3' : range(3),
        'board_positions': board_positions
    }
    return render(request, 'game_board.html', context)



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required
import json

# views.py
def game_move(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    data = json.loads(request.body)
    position = int(data.get("position"))
    current_user = request.user

    # Check if it's the current user's turn
    if game.current_turn != current_user:
        return JsonResponse({"success": False, "error": "Not your turn."})

    # Validate the move
    if game.board[position] != " ":
        return JsonResponse({"success": False, "error": "Cell already occupied."})

    # Make the move
    symbol = "X" if game.player1 == current_user else "O"
    game.board[position] = symbol

    # Check for a win or draw
    winner = check_winner(game.board)
    if winner:
        game.status = "finished"
        game.winner = current_user
    elif all(cell != " " for cell in game.board):
        game.status = "finished"  # Game is a draw
        winner = None
    else:
        # Change the turn
        game.current_turn = game.player1 if current_user == game.player2 else game.player2

    game.save()

    return JsonResponse({
        "success": True,
        "symbol": symbol,
        "game_over": game.status == "finished",
        "winner": current_user.username if winner else None,
    })


def check_winner(board):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ]
    for pattern in win_patterns:
        a, b, c = pattern
        if board[a] != " " and board[a] == board[b] == board[c]:
            return True
    return False

def game_status(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return JsonResponse({
        "board": list(game.board),  # Return the board as a list
        "current_turn": game.current_turn.username,
        "status": game.get_status_display(),
        "winner": game.winner.username if game.winner else None,
    })

@csrf_exempt
def make_move(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    data = json.loads(request.body)
    position = int(data.get('position', -1))

    # Validate position
    if position < 0 or position >= 9:
        return JsonResponse({"success": False, "error": "Invalid position!"})

    if game.board[position] != " ":
        return JsonResponse({"success": False, "error": "Cell already occupied!"})

    # Validate turn
    if game.current_turn != request.user:
        return JsonResponse({"success": False, "error": "Not your turn!"})

    # Determine the player's symbol
    symbol = "X" if game.current_turn == game.player1 else "O"

    # Update board
    board = list(game.board)
    board[position] = symbol
    game.board = board

    # Check winner and update status
    if check_winner(board):
        game.winner = game.current_turn  # Assign winner as current player
        game.status = "finished"
    elif " " not in board:
        game.status = "finished"  # It's a draw
    else:
        # Switch turns
        game.current_turn = game.player1 if game.current_turn == game.player2 else game.player2

    game.save()

    return JsonResponse({
        "success": True,
        "symbol": symbol,
        "game_over": game.status == "finished",
        "winner": game.winner.username if game.winner else None,
    })