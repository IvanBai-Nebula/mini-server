from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from .models import MediaFile
from django.views.decorators.csrf import csrf_exempt


def upload_file(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type')  # 获取文件类型

        if file:
            media_file = MediaFile.objects.create(title=title, file=file, file_type=file_type)
            return JsonResponse({"success": True, "file_url": media_file.file.url})

    return JsonResponse({"success": False, "message": "文件上传失败"}, status=400)
