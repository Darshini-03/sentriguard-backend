from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict),
    path('history/', views.get_history),
    path('image/', views.image_predict),
    path('register/', views.register_user),
path('login/', views.login_user),
path('logout/', views.logout_user),
path('delete/<int:id>/', views.delete_prediction),
path('clear/', views.clear_history),
]

