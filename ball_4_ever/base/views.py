from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm
from .models import Question, Comment, Like, DisLike
from posts.models import Post


def is_valid_query_param(param):
    return param != '' and param is not None


def filter_list(obj, context):
    category = obj.request.GET.get('category')

    if is_valid_query_param(category) and category != 'Votes':
        if category == 'time_desc':
            context['comments'] = context['question'].comment.all().order_by('-date_created')
        else:
            context['comments'] = context['question'].comment.all().order_by('date_created')
    else:
        context['comments'] = reversed(sorted(context['question'].comment.all(), key=lambda a: a.rating))

    return context


def home(request):
    questions = Question.objects.order_by("-date_created")[:3]
    posts = Post.objects.order_by("-date_created")[:3]
    context = {'questions': questions, 'posts': posts}

    return render(request, "home.html", context=context)


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = "base/questions_list.html"
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-title') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context


class MyQuestionListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    template_name = "base/questions_list.html"
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = context['questions'].filter(user=self.request.user)
        search_input = self.request.GET.get('search-title') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains=search_input)
        return context


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = "base/question_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = filter_list(self, context)
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'content']
    template_name = "base/question_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'content']
    template_name = "base/question_update.html"

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class CommentAddView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'base/question_answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)


class UpdateCommentVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id', None)
        opinion = self.kwargs.get('opinion', None)
        comment = get_object_or_404(Comment, id=comment_id)
        # import pdb
        # pdb.set_trace()

        try:
            comment.dis_likes
        except Comment.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(comment=comment)

        try:
            comment.likes
        except Comment.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(comment=comment)

        if opinion == 'like':
            if request.user in comment.likes.users.all():
                comment.likes.users.remove(request.user)
            else:
                comment.likes.users.add(request.user)
                comment.dis_likes.users.remove(request.user)

        elif opinion == 'dis_like':

            if request.user in comment.dis_likes.users.all():
                comment.dis_likes.users.remove(request.user)
            else:
                comment.dis_likes.users.add(request.user)
                comment.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('base:question_details', args=(comment.question.id,)))
        return HttpResponseRedirect(reverse('base:question_details', args=(comment.question.id,)))
