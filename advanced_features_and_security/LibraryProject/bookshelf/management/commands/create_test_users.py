from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from bookshelf.models import CustomUser
from datetime import date


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups'

    def handle(self, *args, **options):
        self.stdout.write('Creating test users and assigning groups...')
        
        # Get groups
        try:
            viewers_group = Group.objects.get(name='Viewers')
            editors_group = Group.objects.get(name='Editors')
            admins_group = Group.objects.get(name='Admins')
        except Group.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Group not found: {e}'))
            self.stdout.write('Please run "python manage.py setup_groups" first.')
            return
        
        # Create test users
        test_users = [
            {
                'username': 'viewer_user',
                'email': 'viewer@example.com',
                'first_name': 'Viewer',
                'last_name': 'User',
                'date_of_birth': date(1990, 1, 1),
                'groups': [viewers_group],
                'password': 'viewer123'
            },
            {
                'username': 'editor_user',
                'email': 'editor@example.com',
                'first_name': 'Editor',
                'last_name': 'User',
                'date_of_birth': date(1985, 5, 15),
                'groups': [editors_group],
                'password': 'editor123'
            },
            {
                'username': 'admin_user',
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'date_of_birth': date(1980, 10, 20),
                'groups': [admins_group],
                'password': 'admin123'
            },
            {
                'username': 'no_permissions_user',
                'email': 'noperms@example.com',
                'first_name': 'No',
                'last_name': 'Permissions',
                'date_of_birth': date(1995, 3, 10),
                'groups': [],
                'password': 'noperms123'
            }
        ]
        
        for user_data in test_users:
            username = user_data['username']
            groups = user_data.pop('groups')
            password = user_data.pop('password')
            
            # Delete existing user if exists
            CustomUser.objects.filter(username=username).delete()
            
            # Create new user
            user = CustomUser.objects.create_user(
                username=username,
                email=user_data['email'],
                password=password,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                date_of_birth=user_data['date_of_birth']
            )
            
            # Assign groups
            for group in groups:
                user.groups.add(group)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created user: {username} (password: {password}) - Groups: {[g.name for g in groups]}'
                )
            )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('TEST USERS CREATED:')
        self.stdout.write('='*60)
        self.stdout.write('1. viewer_user (password: viewer123) - Viewers group')
        self.stdout.write('   - Can view books, authors, libraries')
        self.stdout.write('   - Cannot create, edit, or delete')
        self.stdout.write('')
        self.stdout.write('2. editor_user (password: editor123) - Editors group')
        self.stdout.write('   - Can view, create, and edit books, authors, libraries')
        self.stdout.write('   - Cannot delete')
        self.stdout.write('')
        self.stdout.write('3. admin_user (password: admin123) - Admins group')
        self.stdout.write('   - Can perform all actions (view, create, edit, delete)')
        self.stdout.write('')
        self.stdout.write('4. no_permissions_user (password: noperms123) - No groups')
        self.stdout.write('   - No permissions assigned')
        self.stdout.write('')
        self.stdout.write('You can now test the permission system by:')
        self.stdout.write('1. Starting the server: python manage.py runserver')
        self.stdout.write('2. Going to /admin/ and logging in with different users')
        self.stdout.write('3. Testing the bookshelf views at /bookshelf/')
        self.stdout.write('='*60)
