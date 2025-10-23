from django.utils.version import get_version
from .version import APP_VERSION

__version__ = get_version(tuple(APP_VERSION))