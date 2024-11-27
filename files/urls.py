from django.urls import path
from .views import FileUploadView, FileDownloadView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload-file'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='download-file'),
]
