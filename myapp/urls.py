from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('api/user/recommend-product/<str:id>/', views.get_data, name='get_data'),
]