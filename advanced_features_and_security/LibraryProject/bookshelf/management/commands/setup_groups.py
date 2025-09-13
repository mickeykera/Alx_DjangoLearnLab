from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book
from relationship_app.models import Author, Library


class Command(BaseCommand):
    help = 'Set up user groups with appropriate permissions'

    def handle(self, *args, **options):
        self.stdout.write('Setting up user groups and permissions...')
        
        # Get content types for our models
        book_content_type = ContentType.objects.get_for_model(Book)
        author_content_type = ContentType.objects.get_for_model(Author)
        library_content_type = ContentType.objects.get_for_model(Library)
        
        # Get all permissions for our models
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        author_permissions = Permission.objects.filter(content_type=author_content_type)
        library_permissions = Permission.objects.filter(content_type=library_content_type)
        
        # Create Viewers group
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Viewers group'))
        else:
            self.stdout.write('Viewers group already exists')
        
        # Assign view permissions to Viewers
        view_permissions = Permission.objects.filter(
            content_type__in=[book_content_type, author_content_type, library_content_type],
            codename__in=['can_view', 'view_book', 'view_author', 'view_library']
        )
        viewers_group.permissions.set(view_permissions)
        self.stdout.write(f'Assigned {view_permissions.count()} view permissions to Viewers')
        
        # Create Editors group
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editors group'))
        else:
            self.stdout.write('Editors group already exists')
        
        # Assign create and edit permissions to Editors
        editor_permissions = Permission.objects.filter(
            content_type__in=[book_content_type, author_content_type, library_content_type],
            codename__in=[
                'can_view', 'can_create', 'can_edit',
                'view_book', 'add_book', 'change_book',
                'view_author', 'add_author', 'change_author',
                'view_library', 'add_library', 'change_library'
            ]
        )
        editors_group.permissions.set(editor_permissions)
        self.stdout.write(f'Assigned {editor_permissions.count()} editor permissions to Editors')
        
        # Create Admins group
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        else:
            self.stdout.write('Admins group already exists')
        
        # Assign all permissions to Admins
        all_permissions = Permission.objects.filter(
            content_type__in=[book_content_type, author_content_type, library_content_type]
        )
        admins_group.permissions.set(all_permissions)
        self.stdout.write(f'Assigned {all_permissions.count()} permissions to Admins')
        
        # Display group information
        self.stdout.write('\n' + '='*50)
        self.stdout.write('GROUP PERMISSIONS SUMMARY:')
        self.stdout.write('='*50)
        
        for group in [viewers_group, editors_group, admins_group]:
            self.stdout.write(f'\n{group.name}:')
            permissions = group.permissions.all()
            for perm in permissions:
                self.stdout.write(f'  - {perm.content_type.app_label}.{perm.codename}: {perm.name}')
        
        self.stdout.write('\n' + self.style.SUCCESS('Groups and permissions setup completed!'))
