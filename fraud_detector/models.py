from django.db import models

class Prediction(models.Model):
    message = models.TextField()
    result = models.CharField(max_length=10)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result