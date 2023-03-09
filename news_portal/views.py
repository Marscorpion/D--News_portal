from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import NewsForm
from .models import Post
from .filters import PostFilter

class PostTypeException(Exception):
    pass

class NewsList(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NS'
        return super().form_valid(form)

class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AC'
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.type == 'AC':
            return HttpResponse('Такой статьи не существует')
        post.save()
        return super().form_valid(form)

    class ProtectedView(LoginRequiredMixin, TemplateView):
        template_name = 'news_edit.html'

class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.type == 'NS':
            return HttpResponse('Такой новости не существует')
        post.save()
        return super().form_valid(form)

    class ProtectedView(LoginRequiredMixin, TemplateView):
        template_name = 'article_edit.html'

class NewsDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('news_list')
    template_name = 'news_delete.html'


class ArticleDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('news_list')
    template_name = 'article_delete.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('news_list')


