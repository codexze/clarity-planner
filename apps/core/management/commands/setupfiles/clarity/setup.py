from django.contrib.auth.models import Group
from apps.authorize.models import User

from . import data

def start(cmd):
    cmd.stdout.write(cmd.style.SUCCESS('Creating role: manager'), ending='\n')
    manager, created = Group.objects.get_or_create(name='manager')
    if not created:
        cmd.stdout.write(cmd.style.WARNING('Role: manager already exists'), ending='\n')

    cmd.stdout.write(cmd.style.SUCCESS('Creating role: employee'), ending='\n')
    employee, created = Group.objects.get_or_create(name='employee')
    if not created:
        cmd.stdout.write(cmd.style.WARNING('Role: employee already exists'), ending='\n')

    ##########################################################################################################

    cmd.stdout.write(cmd.style.SUCCESS( 'Creating user: manager'), ending='\n')
    user, created = User.objects.get_or_create(username='manager')
    if created:
        user.first_name = "Manager"
        user.last_name = "Clarity"
        user.email = "manager@clarity.sr"
        user.set_password('admin1')
        user.groups.add(manager)
        user.save()
    else:
        cmd.stdout.write(cmd.style.WARNING('User: manager already exists'), ending='\n')
    
    cmd.stdout.write(cmd.style.SUCCESS( 'Creating user: employeea'), ending='\n')
    user, created = User.objects.get_or_create(username='employeea')
    if created:
        user.first_name = "Emplyee A"
        user.last_name = "Clarity"
        user.email = "a.employee@clarity.sr"
        user.set_password('admin1')
        user.groups.add(employee)
        user.save()
    else:
        cmd.stdout.write(cmd.style.WARNING('User: employeea already exists'), ending='\n')

    cmd.stdout.write(cmd.style.SUCCESS( 'Creating user: employeeb'), ending='\n')
    user, created = User.objects.get_or_create(username='employeeb')
    if created:
        user.first_name = "Employee B"
        user.last_name = "Clarity"
        user.email = "b.employee@clarity.sr"
        user.set_password('admin1')
        user.groups.add(employee)
        user.save()
    else:
        cmd.stdout.write(cmd.style.WARNING('User: employeeb already exists'), ending='\n')

    ##########################################################################################################
    cmd.stdout.write(cmd.style.SUCCESS('SETUP CLARITY DATA'), ending='\n')
    data.inject(cmd)