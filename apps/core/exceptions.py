from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class MissingConsistencyTokenError(Exception):pass
class ConsistencyError(Exception):pass