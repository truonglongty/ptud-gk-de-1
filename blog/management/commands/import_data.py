from django.core.management.base import BaseCommand
from blog.models import Post, Comment, UserProfile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Import data into the database'

    def handle(self, *args, **kwargs):
        # Create a user
        user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
        if created:
            user.set_password('123456')
            user.save()
            UserProfile.objects.create(user=user, role='admin')

        # Create some posts
        post1 = Post.objects.create(title='First Post', content='This is the first post.', author=user)
        post2 = Post.objects.create(title='Second Post', content='This is the second post.', author=user)

        # Create some comments
        Comment.objects.create(post=post1, author=user, text='This is a comment on the first post.')
        Comment.objects.create(post=post2, author=user, text='This is a comment on the second post.')

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))