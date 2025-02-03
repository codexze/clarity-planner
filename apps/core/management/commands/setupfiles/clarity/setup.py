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
        user.first_name = "Clarity"
        user.last_name = "Manager"
        user.email = "manager@clarity.sr"
        user.set_password('admin1')
        user.groups.add(manager)
        user.save()
    else:
        cmd.stdout.write(cmd.style.WARNING('User: manager already exists'), ending='\n')
    
    cmd.stdout.write(cmd.style.SUCCESS( 'Creating user: employee_a'), ending='\n')
    user, created = User.objects.get_or_create(username='employee_a')
    if created:
        user.first_name = "Clarity"
        user.last_name = "Emplyee A"
        user.email = "a.employee@clarity.sr"
        user.set_password('admin1')
        user.groups.add(employee)
        user.save()
    else:
        cmd.stdout.write(cmd.style.WARNING('User: employee_a already exists'), ending='\n')
    
    cmd.stdout.write(cmd.style.SUCCESS( 'Creating user: employee_b'), ending='\n')
    user, created = User.objects.get_or_create(username='employee_b')
    if created:
        user.first_name = "Clarity"
        user.last_name = "EmployeeB"
        user.email = "b.employee@clarity.sr"
        user.set_password('admin1')
        user.groups.add(employee)
        user.save()
    else:
        cmd.stdout.write(cmd.style.WARNING('User: employee_b already exists'), ending='\n')

    ##########################################################################################################
    cmd.stdout.write(cmd.style.SUCCESS('SETUP CLARITY DATA'), ending='\n')
    data.inject(cmd)