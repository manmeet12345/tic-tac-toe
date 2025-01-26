from django.urls import path, include
from . import views

urlpatterns = [
    # Template URLs
    path('', views.home_view, name='home'),
    path('register/',views.register,name="register"),
    path('login/',views.user_login,name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('game_list/', views.game_list, name='game_list'),
    path('game/start/', views.start_game, name='start_game'),
    path('game/new/', views.new_game, name='new_game'),
    path('games/<int:game_id>/', views.game_board, name='game_board'),
    path('game/<int:game_id>/move/', views.make_move, name='game_move'),
    path('game/make_move/<int:game_id>/move/', views.make_move, name='make_move'),
    path('game-status/<int:game_id>/', views.game_status, name='game_status'),
    #path('games/<int:game_id>/forfeit/', views.forfeit_game, name='forfeit_game'),
]