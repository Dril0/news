from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
)  # listview retorna un objeto <model_name>_list del cual podemos iterar. formview muestra el form cualquier error validado y redirecciona a una URL
from django.views.generic.detail import SingleObjectMixin #asocia el articulo con el form
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)  # restringe el acceso a views para los user NO logueados, nos exige loguearnos primero para tener acceso, Userpasses.. restringe el acceso para realizar cambios solo al author del articulo.
from .forms import CommentForm
from django.views import View

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


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"
    
    def get_context_data(self, **kwargs):#actualiza el context(un diccionario quecontiente todas los nombres de variables y valores del template)
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"
    
    def post(self, request, *args, **kwargs):
        self.object =self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk":article.pk})
    pass

class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, requet, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)



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
