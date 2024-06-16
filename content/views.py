from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from content.forms import ContentForm, ManagerContentForm
from content.models import Content, LikeCount, Comment


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
        Добавляет текущего пользователя при создании объекта.
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
        """ Метод добавляет дополнительные поля: лайки и комментарии """
        context = super().get_context_data(**kwargs)
        context['like'] = LikeCount.objects.filter(content__pk=self.object.pk).count()
        context['comments'] = Comment.objects.filter(content__pk=self.object.pk)

        return context


class ContentManagerListView(generic.ListView):
    """
    Контроллер для главной страницы.
    Примимает модель Content.
    """
    model = Content
    template_name = 'content/contentmanager_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Метод выполняющий фильтрацию по наличию публикации.
        Выводит на главную страницу только те блоги, которые имеют положительный признак публикации(True)
        """
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_authenticated or not self.request.user.has_perm('content.change_publish'):
            raise PermissionDenied
        else:
            queryset = queryset.filter(publish=False)
            return queryset



class ContentPersonalListView(generic.ListView):
    """
    Контроллер для главной страницы.
    Примимает модель Content.
    """
    model = Content
    template_name = 'content/contentpersonal_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Метод выполняющий фильтрацию по наличию публикации.
        Выводит на главную страницу только те блоги, которые имеют положительный признак публикации(True)
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
        Выводит на главную страницу только те блоги, которые имеют положительный признак публикации(True)
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
    success_url = reverse_lazy('content:personal_list')

    def get_form_class(self):
        if self.request.user == self.get_object().user:
            return ContentForm
        elif self.request.user.has_perm('content.change_publish'):
            return ManagerContentForm
        else:
            return ContentForm


class ContentDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Контроллер для удаления.
    Примимает модель Content.
    """
    model = Content
    success_url = reverse_lazy('content:personal_list')


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
    content_item = get_object_or_404(Content, pk=pk)
    filter_like = LikeCount.objects.filter(content__pk=content_item.pk).filter(user__pk=request.user.pk).exists()
    if filter_like:
        LikeCount.objects.filter(content__pk=content_item.pk).filter(user__pk=request.user.pk).delete()
    else:
        LikeCount.objects.create(user=request.user, content=content_item)
    return redirect(reverse('content:index'))


def comments(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.method == "POST":
        comment = request.POST.get("comment", None)
        cont = Content.objects.get(pk=pk)
        Comment.objects.create(
            user=request.user,
            content=cont,
            comment=comment
        )
        return redirect(reverse('content:detail', kwargs={'pk': pk}))
