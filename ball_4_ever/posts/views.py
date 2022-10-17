from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm
from .models import Post, Comment, DisLike, Like


def is_valid_query_param(param):
    return param != '' and param is not None


def filter_list(obj, context):
    title_contains = obj.request.GET.get('search-title')
    category = obj.request.GET.get('category')

    if is_valid_query_param(title_contains):
        context['posts'] = context['posts'].filter(title__icontains=title_contains)
    if is_valid_query_param(category) and category != 'All':
        context['posts'] = context['posts'].filter(category=category)

    return context


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "posts/posts_list.html"
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = filter_list(self, context)
        context['page'] = ''
        return context


class MyPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "posts/posts_list.html"
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = context['posts'].filter(user=self.request.user)
        context = filter_list(self, context)
        context['page'] = 'my'
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "posts/post_details.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['back_page'] = 'overall'
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'category', 'title', 'content']
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['image', 'category', 'title', 'content']
    template_name = "posts/post_update.html"

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class CommentAddView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/post_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class UpdatePostVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id', None)
        opinion = self.kwargs.get('opinion', None)
        post = get_object_or_404(Post, id=post_id)

        try:
            post.dis_likes
        except Post.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(post=post)

        try:
            post.likes
        except Post.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(post=post)

        if opinion == 'like':
            if request.user in post.likes.users.all():
                post.likes.users.remove(request.user)
            else:
                post.likes.users.add(request.user)
                post.dis_likes.users.remove(request.user)

        elif opinion == 'dis_like':

            if request.user in post.dis_likes.users.all():
                post.dis_likes.users.remove(request.user)
            else:
                post.dis_likes.users.add(request.user)
                post.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('posts:post_details', args=(post.id,)))

        return HttpResponseRedirect(reverse('posts:post_details', args=(post.id,)))
