from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import FileSerializer
from .models import File

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.first_name != 'ops':
            return Response({"error": "Only ops users can upload files."}, status=403)

        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response({"message": "File uploaded successfully!"}, status=201)

        return Response(serializer.errors, status=400)

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        file = get_object_or_404(File, id=file_id)
        if request.user.first_name != 'client':
            return Response({"error": "Only clients can download files."}, status=403)

        download_url = f"http://localhost:8000/media/{file.file}"
        return Response({"download-link": download_url, "message": "success"})
