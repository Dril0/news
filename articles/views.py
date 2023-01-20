from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)  # listview retorna un objeto <model_name>_list del cual podemos iterar.
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)  # restringe el acceso a views para los user NO logueados, nos exige loguearnos primero para tener acceso, Userpasses.. restringe el acceso para realizar cambios solo al author del articulo.

# Create your views here.


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    fields = (
        "title",
        "body",
    )
    """Setea automaticamente como author al usuario actualmente logueado"""

    def form_valid(
        self, form
    ):  # nos permite sobreescribir para lograr el resultado deseado en vez de reescribir todo. en este caso el usuario que ya esta logueado.
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ("title", "body")
    template_name = "article_edit.html"
    """si el author del actual objeto coincide con el usuario logueado permite realizar los cambios. sino tira error."""

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")
    """si el author del actual objeto coincide con el usuario logueado permite realizar los cambios. sino tira error."""

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
