from PIL import Image
from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField


class Post(models.Model):
    CHOICES = (
        ("Shooting", "Shooting"),
        ("Finishing", "Finishing"),
        ("Dribbling", "Dribbling"),
        ("Athleticism", "Athleticism"),
        ("Injuries", "Injuries"),
        ("Defence", "Defence"),
        ("TeamPlay", "TeamPlay"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=25, choices=CHOICES, default="Shooting")
    image = models.ImageField(default='default.jpg', upload_to="post_pic")
    title = models.CharField(max_length=10000)
    content = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - Post'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            print(self.image.path)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('posts:post_details', kwargs={'pk': self.pk})

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)
    content = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.post.user)

    def get_absolute_url(self):
        return reverse('posts:post_details', kwargs={'pk': self.post.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Like(models.Model):
    post = models.OneToOneField(Post, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.answer)[:30]


class DisLike(models.Model):
    post = models.OneToOneField(Post, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_post_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.answer)[:30]
