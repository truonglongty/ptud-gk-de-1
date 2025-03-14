from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post

@receiver(post_migrate)
def create_sample_posts(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_user(username='admin', email='admin@example.com', password='123456')

        # Tạo 5 bài post
        for i in range(5):
            Post.objects.create(title=f'Post {i+1}', content=f'This is post number {i+1}.', author=user)