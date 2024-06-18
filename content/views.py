from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic

from content.forms import ContentForm, ManagerContentForm
from content.models import Content, LikeCount, Comment


def get_search_content(request):
    """
    Функция для осуществления поиска по запросу пользователя.
    Принимает текст запроса и ищет его в заголовке или описании.
    """
    if request.method == "POST":
        search = request.POST.get("search", None)
        search_content_text = Content.objects.filter(text__icontains=search)
        if search_content_text:
            return render(request, 'content/searchcontent_list.html',
                          {'search_content_text': search_content_text})
        else:
            search_content_text = Content.objects.filter(title__icontains=search)
            return render(request, 'content/searchcontent_list.html',
                          {'search_content_text': search_content_text})


def get_statistics(request):
    """
    Функция для подсчёта статистики постов пользователя.
    Возвращает словарь с объектами статистики.
    """
    # Получаем количество всех постов пользователя
    post_all = Content.objects.filter(user=request.user).count()
    # Получаем пост с самым высоким колличеством просмотров
    filter_views = Content.objects.filter(user=request.user).order_by('-views').first()
    # Получаем пост с самым большим колличеством лайков
    pk_post = 0
    count_likes = 0
    content_filter = Content.objects.filter(user=request.user)
    for content_pk in content_filter:
        like_filter = LikeCount.objects.filter(content__pk=content_pk.pk).count()
        if count_likes <= like_filter:
            count_likes = like_filter
            pk_post = content_pk.pk
    max_likes = Content.objects.get(pk=pk_post)

    return render(request, 'content/statistics.html',
                  {'post_all': post_all, 'post_views': filter_views, 'post_likes': max_likes})


class ContentCreateView(generic.CreateView):
    """
    Контроллер для создания контента.
    Примимает модель Content.
    Форма ContentForm.
    """
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('content:index')

    def form_valid(self, form):
        """
        Метод при успешном создании.
        Если пользователь авторизован -
        Добавляет текущего пользователя при создании объекта.
        Меняет флаг публикации на положительный.
        """
        if form.is_valid():
            new_content = form.save(commit=False)
            if self.request.user.is_authenticated:
                new_content.user = self.request.user
                new_content.publish = True
                new_content.save()
            else:
                new_content.save()
        return super().form_valid(form)


class ContentDetailView(generic.DetailView):
    """
    Контроллер для детального просмотра контента.
    Примимает модель Content.
    """
    model = Content

    def get_object(self, queryset=None):
        """
        Метод для накрутки просмотров.
        Добавляет к полю +1 при каждом обновлении страницы.
        """
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        """
        Метод добавляет отображение дополнительных полей:
        Лайки и комментарии.
        """
        context = super().get_context_data(**kwargs)
        context['like'] = LikeCount.objects.filter(content__pk=self.object.pk).count()
        context['comments'] = Comment.objects.filter(content__pk=self.object.pk)

        return context


class ContentManagerListView(generic.ListView):
    """
    Контроллер для страницы менеджеров.
    Примимает модель Content.
    """
    model = Content
    template_name = 'content/contentmanager_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Метод выполняющий фильтрацию по наличию публикации.
        Выводит на страницу только те посты,
        Которые имеют отрицательныйпризнак публикации(False).
        Перекрывает доступ пользователям без прав на изменение публикации
        И не авторизованным пользователям.
        """
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_authenticated or not self.request.user.has_perm('content.change_publish'):
            raise PermissionDenied
        else:
            queryset = queryset.filter(publish=False)
            return queryset


class ContentPersonalListView(generic.ListView):
    """
    Контроллер для страницы личных постов.
    Примимает модель Content.
    """
    model = Content
    template_name = 'content/contentpersonal_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Метод выполняющий фильтрацию по текущему пользователю.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ContentListView(generic.ListView):
    """
    Контроллер для главной страницы.
    Примимает модель Content.
    """
    model = Content
    template_name = 'content/home_page.html'

    def get_queryset(self, *args, **kwargs):
        """
        Метод выполняющий фильтрацию по наличию публикации.
        Выводит на главную страницу только те посты,
        Которые имеют положительный признак публикации(True).
        Добавляет поле маркера лайка.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publish=True)
        for query in queryset:
            if LikeCount.objects.filter(content__pk=query.pk).filter(user__pk=self.request.user.pk).exists():
                query.like_mark = True
        return queryset


class ContentUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Контроллер для редактирования.
    Примимает модель Content.
    Форма ContentForm.
    """
    model = Content
    form_class = ContentForm

    def get_form_class(self):
        """
        Метод возвращает форму ContentForm,
        Если пользователь является автором поста.
        Если у пользователя есть права на изменение поста,
        То возвращает форму ManagerContentForm.
        """
        if self.request.user == self.get_object().user:
            return ContentForm
        elif self.request.user.has_perm('content.change_publish'):
            return ManagerContentForm
        else:
            return ContentForm

    def get_success_url(self):
        """
        Метод возвращает адрес страницы при успешном изменении поста.
        Если пользователь является автором поста,
        Перенаправляет на страницу личных постов.
        Если пользователь имеет права на изменение поста,
        Перенаправляет на страницу менеджеров.
        """
        if self.request.user == self.get_object().user:
            return reverse('content:personal_list')
        elif self.request.user.has_perm('content.change_publish'):
            return reverse('content:manager_list')


class ContentDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Контроллер для удаления.
    Примимает модель Content.
    """
    model = Content
    success_url = reverse_lazy('content:personal_list')

    def get_object(self, queryset=None):
        """
        Метод при удалении объекта.
        Выводит ошибку если пользователь не является автором поста,
        Или не авторизовался в системе.
        """
        self.object = super().get_object(queryset)
        if not self.request.user.is_authenticated or self.request.user != self.object.user:
            raise PermissionDenied


def likes(request, pk):
    """
    Функция для добавления или удаление лайков.
    Доступна только для авторизованных пользователей.
    Если пользователь не авторизован, вызывает исключение.
    Получает индицикатор текущего поста, находит его в базе.
    Выполняется фильтрация по модели LikeCount.
    Если у текущего поста потльзователь добавил лайк, то удаляет его.
    Если пользователь еще не добавил лайк, то добавляет его.
    Перенаправляет на главную страницу.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied
    filter_like = LikeCount.objects.filter(content__pk=pk, user__pk=request.user.pk).exists()
    if filter_like:
        LikeCount.objects.filter(content__pk=pk).filter(user__pk=request.user.pk).delete()
    else:
        LikeCount.objects.create(user=request.user, content=Content.objects.get(pk=pk))
    return redirect(reverse('content:index'))


def comments(request, pk):
    """"
    Функция для добавления комментариев в базу данных.
    Доступна только для авторизованных пользователей.
    Принимает текст комментария и создает модель Comment.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == "POST":
        comment = request.POST.get("comment", None)
        Comment.objects.create(
            user=request.user,
            content=Content.objects.get(pk=pk),
            comment=comment
        )
        return redirect(reverse('content:detail', kwargs={'pk': pk}))
