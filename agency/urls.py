from django.urls import path
from . import views

urlpatterns = [
    # Spy Cat endpoints
    path('cats/', views.SpyCatListCreateView.as_view(), name='cat-list-create'),
    path('cats/<int:pk>/', views.SpyCatDetailView.as_view(), name='cat-detail'),
    path('cats/<int:pk>/salary/', views.SpyCatUpdateSalaryView.as_view(), name='cat-update-salary'),
    path('cats/available/', views.available_cats, name='available-cats'),
    

]
