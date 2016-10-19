from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from blog.models import Article
from comment.models import Comments
from navigation.models import Category, MenuItem
from blog.form import SendMassageForm, ArticleForm
from comment.forms import CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from loginsys.models import Profile
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory, inlineformset_factory
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, FormView


# articles list in class

class ArticleList(ListView):
    # model = Article
    # queryset = Article.objects.order_by('-article_date')
    template_name = 'gallery_works_api.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.category = get_object_or_404(Category, menu_category__menu_name=self.kwargs['item_slug'],
                                          category_name=self.kwargs['category_slug'])
        articles_list = Article.objects.filter(article_category=self.category).order_by('-article_date')
        query = self.request.GET.get('q')
        if query:
            articles_list = Article.objects.filter(
                Q(article_title__icontains=query) |
                Q(article_text__icontains=query)).distinct()
            return articles_list
        return articles_list

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['articles_carousel'] = self.category.articles.all().order_by('-article_likes')[0:3]
        return context


# class ArticleCommentForm(View):
#     model = Comments
#     form_class = CommentForm
#     context_object_name = 'comments'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#
#             return HttpResponseRedirect(self.article.get_absolute_url())
#         return render(request, self.template_name, {'form': form})


class ArticleDetail(SingleObjectMixin, FormView):
    model = Article
    template_name = 'gallery_work_api.html'
    context_object_name = 'comments'
    slug_field = 'article_slug'
    slug_url_kwarg = 'article_slug'
    form_class = CommentForm
    paginate_by = 3

    def get_success_url(self):
        return reverse('blog:api:article_detail', kwargs={'item_slug': self.kwargs['item_slug'],
                                                          'category_slug': self.kwargs['category_slug'],
                                                          'article_slug': self.kwargs['article_slug']})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Article.objects.all())
        return super(ArticleDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        comments_list = self.object.comments.all().order_by('-comments_create')
        current_page = Paginator(comments_list, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context['form'] = self.get_form(form_class)
        context['article'] = self.object
        context['comments'] = current_page.page(page_number)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404(_('Ви немаєте прав для запису коментарів!'))
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if 'pause' in self.request.session:
            messages.error(self.request, _('Ви вже залишили коментар, зачекайте хвилину.'), extra_tags='error')
            return self.form_invalid(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if not self.request.user.is_staff or not self.request.user.is_authenticated:
            raise Http404(_('Ви немаєте прав для створення статті!'))
        else:
            form.instance.comments_article = self.object
            form.instance.comments_user = get_object_or_404(Profile, user=self.request.user)
            form.save()
            self.request.session.set_expiry(60)
            self.request.session['pause'] = True
            messages.success(self.request, _('Коментар добавлений успішно!'), extra_tags='success')
            return super(ArticleDetail, self).form_valid(form)

# class ArticleDetail(SingleObjectMixin, ListView):
#     template_name = 'gallery_work_api.html'
#     # context_object_name = 'comments'
#     slug_field = 'article_slug'
#     slug_url_kwarg = 'article_slug'
#     form_class = CommentForm
#     paginate_by = 2
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(queryset=Article.objects.all())
#         return super(ArticleDetail, self).get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             raise Http404(_('Ви немаєте прав для запису коментарів!'))
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect(self.object.get_absolute_url())
#         else:
#             return render(request, self.template_name, self.get_context_data())
#
#     def form_valid(self, form):
#         if not self.request.user.is_staff or not self.request.user.is_authenticated:
#             raise Http404(_('Ви немаєте прав для створення статті!'))
#         if 'pause' in self.request.session:
#             messages.error(self.request, _('Ви вже залишили коментар, зачекайте хвилину.'), extra_tags='error')
#         else:
#             form.instance.comments_article = self.object
#             form.instance.comments_user = get_object_or_404(Profile, user=self.request.user)
#             self.request.session.set_expiry(60)
#             self.request.session['pause'] = True
#             messages.success(self.request, _('Коментар добавлений успішно!'), extra_tags='success')
#             return super(ArticleCreate, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(ArticleDetail, self).get_context_data(**kwargs)
#         context['form'] = self.form_class
#         context['article'] = self.object
#         return context
#
#     def get_queryset(self):
#         return self.object.comments.all()


# class ArticleDetail(DetailView):
#     model = Comments
#     template_name = 'gallery_work_api.html'
#     context_object_name = 'comments'
#     slug_field = 'article_slug'
#     slug_url_kwarg = 'article_slug'
#
#     def get_queryset(self):
#         self.article = get_object_or_404(Article, article_category__menu_category__menu_name=self.kwargs['item_slug'],
#                                          article_category__category_name=self.kwargs['category_slug'],
#                                          article_slug=self.kwargs['article_slug'])
#         return Comments.objects.filter(comments_article=self.article).order_by('-comments_create')
#
#     def get_context_data(self, **kwargs):
#         context = super(ArticleCommentDetail, self).get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         context['article'] = self.article
#         return context


def user_is_superuser(cl):
    """
    It`s my own decorator which check user. User must be superuser
    """
    def inner(request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404(_('Ви немаєте прав для створення статті!'))
        else:
            return cl(request, *args, **kwargs)
    return inner


class ArticleCreate(CreateView):
    model = Article
    template_name = 'article_form_api.html'
    form_class = ArticleForm

    @method_decorator(user_is_superuser)
    def dispatch(self, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if not self.request.user.is_staff or not self.request.user.is_superuser:
            raise Http404(_('Ви немаєте прав для створення статті!'))
        else:
            form.instance.article_user = get_object_or_404(Profile, user=self.request.user)
            return super(ArticleCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        context['title'] = _('Форма для створення статті')
        context['button_create'] = _('створити статтю')
        context['button_cancel'] = _('відміна')
        context['return_path'] = get_object_or_404(Category,  menu_category__menu_name=self.kwargs['item_slug'],
                                                   category_name=self.kwargs['category_slug']).get_absolute_url()
        return context


class ArticleUpdate(UpdateView):
    model = Article
    template_name = 'article_form_api.html'
    form_class = ArticleForm
    slug_field = 'article_slug'
    slug_url_kwarg = 'article_slug'

    @method_decorator(user_is_superuser)
    def dispatch(self, *args, **kwargs):
        return super(ArticleUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if not self.request.user.is_staff or not self.request.user.is_superuser:
            raise Http404(_('Ви немаєте прав для створення статті!'))
        else:
            form.instance.article_user = get_object_or_404(Profile, user=self.request.user)
            return super(ArticleUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['title'] = _('Форма оновлення статті')
        context['button_create'] = _('змінити статтю')
        context['button_cancel'] = _('відміна')
        context['return_path'] = get_object_or_404(Category,  menu_category__menu_name=self.kwargs['item_slug'],
                                                   category_name=self.kwargs['category_slug']).get_absolute_url()
        return context


class ArticleDelete(DeleteView):
    model = Article
    template_name = 'article_delete_form_api.html'
    slug_field = 'article_slug'
    slug_url_kwarg = 'article_slug'
    success_url = reverse_lazy('blog:api:article_list')

    @method_decorator(user_is_superuser)
    def dispatch(self, *args, **kwargs):
        return super(ArticleDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('blog:api:article_list', kwargs={'item_slug': self.kwargs['item_slug'],
                                                        'category_slug': self.kwargs['category_slug']})

    def form_valid(self, form):
        if not self.request.user.is_staff or not self.request.user.is_superuser:
            raise Http404(_('Ви немаєте прав для видалення статті!'))
        else:
            form.instance.article_user = get_object_or_404(Profile, user=self.request.user)
            return super(ArticleDelete, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleDelete, self).get_context_data(**kwargs)
        context['title'] = _('Ви впевнені, що хочете видалити дану статтю?')
        context['button_delete'] = _('видалити статтю')
        context['button_cancel'] = _('відміна')
        context['return_path'] = get_object_or_404(Category,  menu_category__menu_name=self.kwargs['item_slug'],
                                                   category_name=self.kwargs['category_slug']).get_absolute_url()
        return context




