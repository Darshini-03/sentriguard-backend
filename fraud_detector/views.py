from .models import Prediction

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import joblib
import json
import pytesseract
from PIL import Image
import os

# ✅ SAFE PATH FOR MODEL FILES
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))

# ✅ Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 🔹 TEXT / EMAIL PREDICTION
@csrf_exempt
def predict(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")

        X = vectorizer.transform([message])
        prediction = model.predict(X)[0]
        prob = model.predict_proba(X)[0]

        if prediction == 1:
            result = "Fraud"
            confidence = prob[1]
        else:
            result = "Genuine"
            confidence = prob[0]

        # ✅ SAVE TO DATABASE
        Prediction.objects.create(
            message=message,
            result=result,
            confidence=round(float(confidence), 2)
        )

        return JsonResponse({
            "prediction": result,
            "confidence": round(float(confidence), 2)
        })

    return JsonResponse({"error": "Only POST method allowed"})


# 🔹 IMAGE (OCR) PREDICTION
@csrf_exempt
def image_predict(request):
    if request.method == "POST":
        try:
            file = request.FILES.get('image')

            if not file:
                return JsonResponse({"error": "No image uploaded"})

            img = Image.open(file)

            # Extract text
            text = pytesseract.image_to_string(img)

            # ML prediction
            X = vectorizer.transform([text])
            prediction = model.predict(X)[0]
            prob = model.predict_proba(X)[0]

            if prediction == 1:
                result = "Fraud"
                confidence = prob[1]
            else:
                result = "Genuine"
                confidence = prob[0]

            # ✅ SAVE TO DATABASE
            Prediction.objects.create(
                message=text,
                result=result,
                confidence=round(float(confidence), 2)
            )

            return JsonResponse({
                "extracted_text": text,
                "prediction": result,
                "confidence": round(float(confidence), 2)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Only POST allowed"})


# 🔹 HISTORY
def get_history(request):
    data = list(Prediction.objects.values())
    return JsonResponse(data, safe=False)


# 🔹 REGISTER
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "User already exists"})

        User.objects.create_user(username=username, password=password)
        return JsonResponse({"status": "User created"})

    return JsonResponse({"error": "Only POST allowed"})


# 🔹 LOGIN
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({"status": "Login successful"})
        else:
            return JsonResponse({"status": "Invalid credentials"})

    return JsonResponse({"error": "Only POST allowed"})


# 🔹 LOGOUT
def logout_user(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


# 🔹 DELETE ONE
@csrf_exempt
def delete_prediction(request, id):
    if request.method == "DELETE":
        try:
            obj = Prediction.objects.get(id=id)
            obj.delete()
            return JsonResponse({"status": "Deleted"})
        except:
            return JsonResponse({"error": "Not found"})


# 🔹 CLEAR ALL
@csrf_exempt
def clear_history(request):
    if request.method == "DELETE":
        Prediction.objects.all().delete()
        return JsonResponse({"status": "All history cleared"})
    
    

