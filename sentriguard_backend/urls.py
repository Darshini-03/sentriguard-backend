from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "message": "SentriGuard AI Backend Running Successfully"
    })


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('fraud_detector.urls')),
]

