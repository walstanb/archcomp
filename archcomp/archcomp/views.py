import os
import uuid
import hashlib
import json
import redis
from rq import Queue
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, QueryDict
from django.http import HttpResponse, Http404
from django.core.files import File
from django.conf import settings
from archcomp.tasks import process_file
from .models import UploadedFile


def upload_file(request):
    if request.method == "POST":
        if request.FILES:
            file = request.FILES["file"]
            # Generate a unique ID for the file
            # file_uuid = str(uuid.uuid4())
            md5_hash = hashlib.md5()

            for chunk in file.chunks():
                md5_hash.update(chunk)

            file_uuid = md5_hash.hexdigest()

            # Save the file to disk
            folder_path = os.path.join(settings.MEDIA_ROOT, file_uuid)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            file_name = os.path.join(folder_path, file.name)
            if not os.path.exists(file_name):
                with open(file_name, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Save the file info to the database
                uploaded_file = UploadedFile.objects.create(
                    uuid=file_uuid,
                    filename=file.name,
                    ip_address=request.META["REMOTE_ADDR"],
                    folderpath=folder_path,
                )
                uploaded_file.save()

                # Enqueue a job to process the file
                q = Queue(
                    connection=redis.Redis(
                        host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT,
                        db=settings.REDIS_DB,
                    ),
                    default_timeout=300,
                )
                q.enqueue(process_file, str(uploaded_file))

            # Return the UUID to the frontend
            return JsonResponse({"job_id": file_uuid})
    return render(request, "upload_file.html")


def download_file(request, uuid, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, uuid, filename)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response[
                "Content-Disposition"
            ] = "attachment; filename=" + os.path.basename(file_path)
            return response
    raise Http404


@csrf_exempt
def get_status(request, uuid):
    if request.method == "GET":
        try:
            # Retrieve the job status from Redis
            uploaded_file = UploadedFile.objects.get(uuid=uuid)
            status = uploaded_file.status
            if status == "success":
                file_list = list(os.listdir(uploaded_file.folderpath))
                file_urls = [
                    request.build_absolute_uri(f"/download/{str(uuid)}/{file}")
                    for file in file_list
                    if file.split(".")[-1] == "csv"
                ]
                files = [
                    {"name": file_list[i], "url": file_urls[i]}
                    for i in range(len(file_list))
                ]

                return JsonResponse({"status": status, "files": files})

            if status == "failed":
                return JsonResponse({"status": status})

            # Return the status as JSON
            return JsonResponse({"status": status})
        except Exception as err:
            print(err)
            # If the job ID does not exist in Redis, return a 404 error
            return JsonResponse({"error": f"Job with ID {uuid} does not exist"})

    # elif request.method == 'POST' and request.FILES:
    #     upload_file(request)
