from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('image_predict/', views.image_predict, name='image_predict'),
    path('url_predict/', views.url_predict, name='url_predict'),

    path('history/', views.get_history, name='history'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('delete/<int:id>/', views.delete_prediction, name='delete'),
    path('clear_history/', views.clear_history, name='clear_history'),

    path('validation/', views.model_validation, name='validation'),
    
    path(
        'validation_result/',
        views.validation_result,
        name='validation_result'
    ),
]

