from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.PostListView.as_view(), name='posts_list'),
    path('my/', views.MyPostListView.as_view(), name='my_posts_list'),
    path('new/', views.PostCreateView.as_view(), name="post_create"),

    path('<int:pk>/', views.PostDetailView.as_view(), name='post_details'),

    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('<int:pk>/comment/', views.CommentAddView.as_view(), name="post_comment"),
    path('requirement/<int:post_id>/<str:opinion>/', views.UpdatePostVote.as_view(), name='requirement_post_vote'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
