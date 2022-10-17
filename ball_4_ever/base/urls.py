from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from users import views as user_view
from posts import urls as posts_urls
from django.contrib.auth import views as auth_view


app_name = "base"

urlpatterns = [
    path("", views.home, name="home"),

    path('register/', user_view.register, name="register"),
    path('login/', auth_view.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name="users/logout.html"), name='logout'),

    path('profile/update/', user_view.profile_update, name="profile_update"),
    path('profile/<int:pk>/', user_view.profile, name='profile'),

    path('questions/', views.QuestionListView.as_view(), name='questions_list'),
    path('questions/my', views.MyQuestionListView.as_view(), name='my_questions_list'),

    path('questions/new/', views.QuestionCreateView.as_view(), name='question_create'),

    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name="question_details"),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name="question_update"),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name="question_delete"),

    path('questions/<int:pk>/comment/', views.CommentAddView.as_view(), name="question_comment"),
    path('requirement/<int:comment_id>/<str:opinion>/', views.UpdateCommentVote.as_view(), name='requirement_comment_vote'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
