from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
# from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagsPosts  # , TagsPosts, UploadFiles
from .utils import DataMixin


# Create your views here.

class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Women.publushed.all().select_related('cat')

# @login_required  #(login_url='/')
def about(request):
    contact_list = Women.publushed.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj}
                  )


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # ищем по слагу
    context_object_name = 'post'

    def get_context_data(self, **kwargs):  # делает отображение динамическим, срабатывает во время GET-request
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.publushed, slug=self.kwargs[self.slug_url_kwarg])


class AddPage( DataMixin, CreateView): #LoginRequiredMixin,
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'
    # login_url = 'home' # перенапралвение на другую страницу


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy("thanks")
    title_page = 'Редактирование статьи'


class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = 'women/addpage.html'
    success_url = reverse_lazy("thanks")
    title_page = 'Удаление статьи'


def contact(request):
    return HttpResponse(f'Обратная связь')


def login(request):
    return HttpResponse(f'Авторизация')


def logout(request):
    return HttpResponse(f'Выход')


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.publushed.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):  # делает отображение динамическим, срабатывает во время GET-request
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk
                                      )


class WomenTag(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.publushed.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagsPosts.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title="Тэг: " + tag.tag)


def thanks(request):
    return render(request, 'women/thanks.html')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Ooops! </h1>')