from django.urls import path
from . import views

urlpatterns = [
    path('cats/', views.SpyCatListCreateView.as_view(), name='cat-list-create'),
    path('cats/<int:pk>/', views.SpyCatDetailView.as_view(), name='cat-detail'),
    path('cats/<int:pk>/salary/', views.SpyCatUpdateSalaryView.as_view(), name='cat-update-salary'),
    path('cats/available/', views.available_cats, name='available-cats'),
    
    path('missions/', views.MissionListCreateView.as_view(), name='mission-list-create'),
    path('missions/<int:pk>/', views.MissionDetailView.as_view(), name='mission-detail'),
    path('missions/<int:mission_id>/assign/<int:cat_id>/', views.assign_cat_to_mission, name='assign-cat-to-mission'),
    path('missions/<int:mission_id>/targets/', views.mission_targets, name='mission-targets'),
    
    path('targets/<int:pk>/', views.TargetDetailView.as_view(), name='target-detail'),
]
