from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Create your models here.

class Game(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('draw', 'Draw'),
    )
    
    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.CASCADE)
    board = models.JSONField(default=lambda: [" "] * 9)  # Will store as ['', '', '', '', '', '', '', '', '']
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    winner = models.ForeignKey(User, related_name='games_won', null=True, blank=True, on_delete=models.CASCADE)
    current_turn = models.ForeignKey(User, related_name='games_as_current_turn', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id}: {self.player1.username} vs {self.player2.username}"


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(8)])
    symbol = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Move by {self.player.username} at position {self.position}"
