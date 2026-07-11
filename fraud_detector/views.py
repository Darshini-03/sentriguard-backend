from .models import Prediction
from .url_analyzer import get_domain_age, domain_age_score
from .ssl_checker import check_ssl, ssl_risk_score
from .threat_intel import check_virustotal, virustotal_risk_score
from .safe_browsing import check_safe_browsing, safe_browsing_risk_score
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


# ==========================================
# LOAD MACHINE LEARNING MODEL
# ==========================================

# Safe path for model files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))

# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================
# TEXT / EMAIL FRAUD PREDICTION
# ==========================================
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

        # Save to database
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


# ==========================================
# IMAGE (OCR) FRAUD PREDICTION
# ==========================================
@csrf_exempt
def image_predict(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("image")

            if not file:
                return JsonResponse({"error": "No image uploaded"})

            img = Image.open(file)

            # Extract text from image
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

            # Save to database
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


# ==========================================
# REAL-TIME URL FRAUD DETECTION
# ==========================================
@csrf_exempt
def url_predict(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url", "")

            if not url:
                return JsonResponse({"error": "No URL provided"})

            # 1. WHOIS Domain Age
            age = get_domain_age(url)
            domain_score = domain_age_score(age)

            # 2. SSL Certificate Validation
            ssl_valid = check_ssl(url)
            ssl_score = ssl_risk_score(ssl_valid)

            # 3. VirusTotal Analysis
            detections = check_virustotal(url)
            vt_score = virustotal_risk_score(detections)

            # 4. Google Safe Browsing
            google_flagged = check_safe_browsing(url)
            google_score = safe_browsing_risk_score(google_flagged)

            # 5. Total Risk Score
            total_score = domain_score + ssl_score + vt_score + google_score

            # 6. Final Verdict
            if total_score >= 70:
                verdict = "Fraudulent Website"
            elif total_score >= 20:
                verdict = "Suspicious Website"
            else:
                verdict = "Likely Genuine Website"

            return JsonResponse({
                "url": url,

                # WHOIS
                "domain_age_days": age,
                "domain_risk_score": domain_score,

                # SSL
                "ssl_valid": ssl_valid,
                "ssl_risk_score": ssl_score,

                # VirusTotal
                "virustotal_detections": detections,
                "virustotal_risk_score": vt_score,

                # Google Safe Browsing
                "google_safe_browsing_flagged": google_flagged,
                "google_safe_browsing_risk_score": google_score,

                # Final Result
                "total_risk_score": total_score,
                "verdict": verdict
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Only POST allowed"})
# ==========================================
# HISTORY
# ==========================================
def get_history(request):
    data = list(Prediction.objects.values())
    return JsonResponse(data, safe=False)


# ==========================================
# USER REGISTRATION
# ==========================================
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


# ==========================================
# USER LOGIN
# ==========================================
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


# ==========================================
# USER LOGOUT
# ==========================================
def logout_user(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


# ==========================================
# DELETE ONE HISTORY RECORD
# ==========================================
@csrf_exempt
def delete_prediction(request, id):
    if request.method == "DELETE":
        try:
            obj = Prediction.objects.get(id=id)
            obj.delete()
            return JsonResponse({"status": "Deleted"})
        except Prediction.DoesNotExist:
            return JsonResponse({"error": "Not found"})

    return JsonResponse({"error": "Only DELETE allowed"})


# ==========================================
# CLEAR ALL HISTORY
# ==========================================
@csrf_exempt
def clear_history(request):
    if request.method == "DELETE":
        Prediction.objects.all().delete()
        return JsonResponse({"status": "All history cleared"})

    return JsonResponse({"error": "Only DELETE allowed"})


