from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ActivationView

urlpatterns = [
    path('registers/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('active/<str:email>/<str:activation_code>/', ActivationView.as_view()),        

]