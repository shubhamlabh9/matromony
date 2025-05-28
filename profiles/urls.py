from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('create/', views.CreateProfileView.as_view(), name='create'),
    path('edit/', views.EditProfileView.as_view(), name='edit'),
    path('detail/<int:pk>/', views.ProfileDetailView.as_view(), name='detail'),
    path('my-profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('send-interest/<int:pk>/', views.SendInterestView.as_view(), name='send_interest'),
    path('interests/', views.InterestsView.as_view(), name='interests'),
    path('respond-interest/<int:pk>/', views.RespondInterestView.as_view(), name='respond_interest'),
]
