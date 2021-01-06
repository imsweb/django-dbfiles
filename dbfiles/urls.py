from django.conf import settings
from django.urls import path

from . import views


def dbfiles_url(prefix=settings.MEDIA_URL, view=views.DBFileView.as_view(), name="db_file", **kwargs):
    prefix = prefix.lstrip("/")
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return path("{}<path:name>".format(prefix), view, name=name, kwargs=kwargs)


urlpatterns = [
    dbfiles_url(),
]
