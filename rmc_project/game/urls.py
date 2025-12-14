from django.urls import path
from .views import CreateRoomView, JoinRoomView
from .views import AssignRolesView
from .views import SubmitGuessView
from .views import RoomResultView
from .views import LeaderboardView
from .views import NextRoundView
urlpatterns = [
    path('room/create/', CreateRoomView.as_view(), name='create-room'),
    path('room/join/', JoinRoomView.as_view(), name='join-room'),
     path('room/assign/<int:room_id>/', AssignRolesView.as_view(), name='assign-roles'),
     path('guess/<int:room_id>/', SubmitGuessView.as_view(), name='submit-guess'),
    path('result/<int:room_id>/', RoomResultView.as_view(), name='room-result'),
    path('leaderboard/<int:room_id>/', LeaderboardView.as_view(), name='leaderboard'),
    path('room/next-round/<int:room_id>/', NextRoundView.as_view(), name='next-round'),

]
