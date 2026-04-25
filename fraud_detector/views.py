
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def predict(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")

        if "job" in message.lower():
            result = "Genuine"
            confidence = 0.75
        else:
            result = "Fraud"
            confidence = 0.85

        return JsonResponse({
            "prediction": result,
            "confidence": confidence
        })

    return JsonResponse({"error": "Only POST method allowed"})
