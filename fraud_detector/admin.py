from django.contrib import admin
from .models import Prediction

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('message', 'result', 'confidence', 'created_at')

admin.site.register(Prediction, PredictionAdmin)
