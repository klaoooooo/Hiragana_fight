from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('levels/', views.level_select_view, name='level_select'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('game/<int:level>/', views.game_view, name='game'),
    path('save-score/', views.save_score, name='save_score'),
]