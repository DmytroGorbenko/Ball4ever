from django.contrib import admin
from users.models import Profile
from posts.models import Post
from .models import Question, Comment


admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Post)
