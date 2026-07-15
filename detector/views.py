from django.http import JsonResponse
from django.conf import settings
import os
import json
def validation_result(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        "fraud_detector",
        "validation_result.json"
    )

    if not os.path.exists(file_path):
        return JsonResponse(
            {"error": "validation_result.json not found"},
            status=404
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return JsonResponse(data, safe=False)


