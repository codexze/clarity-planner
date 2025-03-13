
from apps.inhouse.data import *
from apps.clients.data import *
from apps.planning.data import *

def inject(cmd):
    services()
    clients()
    calendar_settings()
    appointments()