import importlib.metadata

__version__ = importlib.metadata.version("django-dbfiles")
__version_info__ = tuple(
    int(num) if num.isdigit() else num for num in __version__.split(".")
)

default_app_config = "dbfiles.apps.DBFilesConfig"
