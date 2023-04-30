
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,DetailView,View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from mkt.forms import UpdateProfileForm,UpdateUserForm,CreateProductForm,CreateCommentForm
from mkt.models import Profile,Product,Category,Comment,Brands

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(SuccessMessageMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'mkt/profile_update_form.html'
    success_url = reverse_lazy("mkt:profile")
    success_message = ("Profile updated!")

    def get_object(self):
        return self.request.user.profile

@login_required
def myprofile(request):
    details = Profile.objects.all()

    my_products = Product.objects.filter(seller=request.user)

    context = {'details':details,
                'my_products':my_products,
    }

    return render(request, 'mkt/profile.html', context)

def sellerprofile(request):
    details = Profile.objects.all()

    my_products = Product.objects.filter(seller=request.user)

    context = {'details':details,
                'my_products':my_products,
    }

    return render(request, 'mkt/seller_profile.html', context)

@method_decorator(login_required, name='dispatch')
class CreateProduct(SuccessMessageMixin, CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'mkt/product_update_form.html'
    success_url = reverse_lazy("mkt:add_product")
    success_message = "Product added Successfully!"

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateProduct(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'mkt/product_edit.html'
    success_url = reverse_lazy("mkt:add_product")
    success_message = "Product updated Successfully!"

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteProduct(SuccessMessageMixin, DeleteView):
    model = Product
    form_class = CreateProductForm
    template_name = 'mkt/delete.html'
    success_url = reverse_lazy("mkt:my_profile")
    success_message = "Product deleted Successfully!"

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

def allcategories(request):
    category = request.GET.get('category')
    category = Category.objects.all().order_by('-name')

    propercat = Product.objects.filter(category__name=category).order_by('-price')

    return render(request, 'mkt/category.html', {
        'category':category,
        'propercat':propercat})

def allbrands(request):
    brand = request.GET.get('brand')
    brand = Brands.objects.all().order_by('-name')

    properbrand = Product.objects.filter(brand__name=brand).order_by('-price')

    return render(request, 'mkt/brands.html', {
        'brand':brand,
        'properbrand':properbrand})

def ProductsView(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    categories = Category.objects.all()
    all_products = Product.objects.all()

    products1 = Product.objects.filter(brand__name=brand).order_by('-price')
    products = Product.objects.filter(category__name=category).order_by('-price')
    
    page_number = request.GET.get(1)
    paginator = Paginator(products, 2)
    page_obj = paginator.get_page(page_number)

    context = {
        'products1':products1,
        'products':products,
        'categories':categories,
        'page_obj':page_obj,
    }

    return render(request, 'mkt/products.html', context)

def ProductDetailView(request, slug):
    product = get_object_or_404(Product, slug=slug)
    seller = request.GET.get('seller_profile')
    category = request.GET.get('category')
    new_comment = None
    comments = Comment.objects.filter(product_id=product, active=True)
    comment_form = CreateCommentForm
    seller = Profile.objects.all()
    related = Product.objects.select_related('seller', 'category')[:5]

    if request.method == "POST":
        comment_form = CreateCommentForm(data=request.POST)
        if comment_form.is_valid():

            comment_form.instance.commentor = request.user

            body = comment_form.cleaned_data['body']

            new_comment = comment_form.save(commit=False)
            new_comment.product = product

            new_comment.save()
        else:
            comment_form = CreateCommentForm()

    return render(request, 'mkt/product_details.html', {
            'product':product,
            'comments':comments,
            'new_comment':new_comment,
            'comment_form':comment_form,
            'seller':seller,
            'related':related,
            })

def homepage(request):
    category = request.GET.get('category')
    promoted = request.GET.get('promoted')

    categories = Category.objects.all().order_by('name')
    brands = Brands.objects.all().order_by('name')
    all_products = Product.objects.all()[:5] 
    products = Product.objects.filter(category__name=category).order_by('name')
    promoted = Product.objects.filter(promoted=True).order_by('name')

    context = {'categories':categories,
                'products':products,
                'all_products':all_products,
                'promoted':promoted,
                'brands':brands,
    }

    return render(request, 'mkt/homepage.html', context)

def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(name__icontains=query) | Q(description__icontains=query)
            qs = Product.objects.filter(lookups)
        else:
            messages.success(request, "No results!")

    return render(request, 'mkt/search_results.html', {'object_list':qs})