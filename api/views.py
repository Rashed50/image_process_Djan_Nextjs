from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import TechStackCard
from django.views import View
import numpy as np
import cv2,base64
from django.views.decorators.csrf import csrf_exempt # for CSRF exemption

class GenerateCard(APIView):
    def post(self, request):
        name = request.data.get('name')
        stacks = request.data.get('stacks')
        return Response({
            "message": f"Card generated for {name} with {len(stacks)} tech stacks"
        })

class SaveCard(APIView):
    def post(self, request):
        name = request.data.get('name')
        stacks = request.data.get('stacks')
        
        if not name or not stacks:
            return Response({"error": "Name and stacks are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        card = TechStackCard.objects.create(name=name, stacks=stacks)
        return Response({"message": "Card saved successfully", "id": card.id}, status=status.HTTP_201_CREATED)
    

class TestEndpoint(APIView):
    def get(self, request):
        cards = TechStackCard.objects.all().values('id', 'name', 'stacks', 'created_at')
        if not cards:
            return Response({"message": "No cards found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"cards": list(cards)}, status=status.HTTP_200_OK)

#class TestEndpoint(APIView):
def hello_api(request):
    data = {
        "status": "success",
        "message": "Hello from Django API",
        "version": "1.0"
    }
    return JsonResponse(data)



@csrf_exempt # Uncomment if you want to disable CSRF protection for this view
def imageProcessing(request):     
    
    data = {
        "status": "success",
        "message": "File Uploaded Successfully",
        "version": "1.0",
        "file_name": request.FILES['file'].name if 'file' in request.FILES else None
    }
    if request.method == "POST" and request.FILES.get("file"):
        # Get uploaded file
        uploaded_file = request.FILES["file"]

        # Read file bytes
        file_bytes = uploaded_file.read()

        # Convert bytes to numpy array
        np_arr = np.frombuffer(file_bytes, np.uint8)

        # Decode image with OpenCV
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Now `img` is an OpenCV image (numpy array)
        # You can do OpenCV processing here
        height, width, channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # return JsonResponse({
        #     "message": "Image received",
        #     "shape": [height, width, channels]
        # })

         # Encode image as PNG in memory
        _, buffer = cv2.imencode(".png", gray)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        # Return as JSON
        return JsonResponse({"image": img_base64})

    return JsonResponse({"error": "No file uploaded"}, status=400)
    return JsonResponse(data)
