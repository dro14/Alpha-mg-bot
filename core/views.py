from django.shortcuts import redirect
from django.http import FileResponse
from alpha.models import Delivery
from django.conf import settings
from re import search
import os


def redirect_view(_):
    return redirect("/admin/login/")


def download_file(_, file_name):
    delivery_id, photo = search(r"^delivery_(\d+)_(photo_\d).jpg$", file_name).groups()
    delivery = Delivery.objects.get(id=int(delivery_id))
    binary = getattr(delivery, photo)
    file_path = settings.MEDIA_ROOT / file_name

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(file_path, "wb") as f:
        f.write(binary)
    return FileResponse(open(file_path, "rb"), content_type="image/jpeg")
