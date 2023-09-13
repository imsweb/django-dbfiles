import mimetypes
import time

import django
from django.http.response import HttpResponse, HttpResponseNotModified
from django.shortcuts import get_object_or_404
from django.utils.http import http_date
from django.views.generic.base import View
from django.views.static import was_modified_since

from .models import DBFile


class DBFileView(View):
    def get(self, request, name):
        db_file = get_object_or_404(DBFile.objects.defer("content"), name=name)

        mtime = time.mktime(db_file.updated_on.timetuple())
        kwargs = {
            "header": self.request.META.get("HTTP_IF_MODIFIED_SINCE"),
            "mtime": mtime,
        }
        if django.VERSION < (4, 1):
            # The `size` parameter was removed in Django 4.1
            kwargs["size"] = db_file.size
        modified = was_modified_since(**kwargs)

        if not modified:
            return HttpResponseNotModified()

        content_type, encoding = mimetypes.guess_type(db_file.name)
        content_type = content_type or "application/octet-stream"

        response = HttpResponse(db_file.content, content_type=content_type)
        response["Last-Modified"] = http_date(mtime)
        response["Content-Length"] = db_file.size
        if encoding:
            response["Content-Encoding"] = encoding
        return response
