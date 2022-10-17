from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from base.models import Question
from posts.models import Post


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully created for {username}! Login In Now')
            return redirect('/login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='/login')
def profile(request, pk):
    # import pdb
    # pdb.set_trace()
    user = User.objects.filter(id=pk)[0]
    posts = Post.objects.filter(user=request.user)
    questions = Question.objects.filter(user=request.user)
    context = {"current": user, 'posts': posts, 'posts_count': len(posts), 'question_count': len(questions)}
    return render(request, 'users/profile.html', context=context)


@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated Successfully!')
            return redirect('base:profile', pk=request.user.id)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile_update.html', context)
