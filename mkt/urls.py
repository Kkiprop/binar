from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mkt import views
from . views import ProfileUpdate,ProductsView,search,allcategories,CreateProduct,myprofile,ProductDetailView,homepage,UpdateProduct,DeleteProduct,sellerprofile,allbrands

app_name = 'mkt'

urlpatterns = [
	path('category/', views.allcategories, name='category'),
	path('brands/', views.allbrands, name='brands'),
	path('home/', views.homepage, name='home'),
	path('products/', views.ProductsView, name='products'),
	path('product_details/<slug>', views.ProductDetailView, name='product_details'),
	path('add_product/', CreateProduct.as_view(), name='add_product'),
	path('edit_product/<slug>', UpdateProduct.as_view(), name='edit_product'),
	path('delete_product/<slug>', DeleteProduct.as_view(), name='delete_product'),
	path('profile/', ProfileUpdate.as_view(), name='profile'),
	path('my_profile/', views.myprofile, name='my_profile'),
	path('seller_profile/', views.sellerprofile, name='seller_profile'),
	path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
