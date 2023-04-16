from django.db import migrations
from django.utils import timezone


def populate_category(apps, schema_editor):
    category_names = ['python', 'sql', 'javascript', 'java', 'c++', 'go']
    categories = []
    Category = apps.get_model('bricabrac', "Category")
    for category in category_names:
        row_to_append = Category(name=category)
        categories.append(row_to_append)

    Category.objects.bulk_create(categories)


def populate_status(apps, schema_editor):
    status_names = ['new', 'easy', 'moderate', 'ratherHard', 'hard']
    statuses = []
    Status = apps.get_model("bricabrac", "Status")
    for status in status_names:
        row_to_append = Status(name=status)
        statuses.append(row_to_append)

    Status.objects.bulk_create(statuses)


def add_user(apps, schema_editor):
    user_details = [{
        'password': 'password',
        'is_superuser': False,
        'username': 'sample_user',
        'first_name': 'sample',
        'last_name': 'user',
        'email': 'sample@user.com',
        'is_staff': False,
        'is_active': True,
        'date_joined': timezone.now()
    }]

    users = []

    User = apps.get_model("auth", "User")
    for user in user_details:
        row_to_append = User(password=user['password'],
                             is_superuser=user['is_superuser'],
                             username=user['username'],
                             first_name=user['first_name'],
                             last_name=user['last_name'],
                             email=user['email'],
                             is_staff=user['is_staff'],
                             is_active=user['is_active'],
                             date_joined=user['date_joined'])
        users.append(row_to_append)

    User.objects.bulk_create(users)


class Migration(migrations.Migration):

    dependencies = [
        ('bricabrac', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_category),
        migrations.RunPython(populate_status),
        migrations.RunPython(add_user),
    ]
