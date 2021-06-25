from django.shortcuts import render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.urls import reverse

from product.models import Product, Category, Comment
from product.forms import CommentForm

# Create your views here.


def index(request):
    return HttpResponse("My Product Page")


class CategoryListView(ListView):
    template_name = 'category_product_list.html'
    paginate_by = 3

    def get_queryset(self):
        products = Product.objects.filter(category__slug=self.kwargs['category'], status=True)
        self.kwargs['count'] = products.count()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['category'])
        context['categories_list'] = Category.objects.all().exclude(slug=context['category'].slug)
        context['product_count'] = self.kwargs['count']
        return context


class ProductListView(ListView):
    template_name = 'all_product_list.html'
    model = Product
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.filter()
        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    form_class = CommentForm
    template_name = 'product_detail.html'

    def get_success_url(self, **kwargs):
        return reverse("product-detail", kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_list'] = Comment.objects.filter(product=self.object)
        context['categories_list'] = Category.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, initial={
            'product': self.object,
            'user': self.request.user
        })

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = Comment(user=form.initial['user'],
                              product=form.initial['product'],
                              **form.cleaned_data)
        new_comment.save()
        return super(ProductDetailView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProductDetailView, self).form_invalid(form)
