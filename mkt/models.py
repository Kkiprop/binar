from django.db import models
from django.contrib.auth.models import Permission, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.shortcuts import reverse
from django_countries.fields import CountryField
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, blank=True, null=True)
	avatar = models.ImageField(upload_to='media/profile', blank=True, null=True)
	about = models.TextField(blank=True, null=True)
	country = CountryField(multiple=False, blank=True, null=True)
	county = models.CharField(max_length=200, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	phone = models.CharField(max_length=200,blank=True, null=True)
	whatsapp = models.CharField(max_length=200, blank=True, null=True)
	facebook = models.URLField(max_length=200, blank=True, null=True)
	instagram = models.URLField(max_length=200, blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.get_or_create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, created, **kwargs):
		if created:
			instance.profile.save()

	def __str__(self):
		return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100,null=True) 
    slug = models.SlugField(unique=True, null=True, editable=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mkt:products", kwargs={
        	'slug':self.slug
		})

class Brands(models.Model):
    name = models.CharField(max_length=100,null=True) 
    slug = models.SlugField(unique=True, null=True, editable=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("mkt:products", kwargs={
        	'slug':self.slug
		})

class Product(models.Model):
	seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	seller_profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True, null=True)
	category = models.ForeignKey(Category, blank=True, null=True, default=False, on_delete=models.CASCADE)
	brand = models.ForeignKey(Brands, blank=True, null=True, default=False, on_delete=models.CASCADE)
	location = models.CharField(max_length=100, blank=True, null=True)
	thumbnail = models.ImageField(upload_to='media/products', blank=True, null=True)
	thumbnail1 = models.ImageField(upload_to='media/products', blank=True, null=True)
	thumbnail2 = models.ImageField(upload_to='media/products', blank=True, null=True)
	price = models.FloatField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)
	slug = models.SlugField(blank=True, null=True)
	instock = models.BooleanField(default=True)
	promoted = models.BooleanField(default=False)

	def __str__(self):
		return self.name 

	def form_valid(self, form):
		form.instance.seller = self.request.user + self.request.user.profile
		return super().form_valid(form)

	def get_absolute_url(self):
		return reverse("mkt:product_details", kwargs={
				'slug':self.slug
			})

class Comment(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
	commentor = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True, null=True)
	avatar = models.ImageField(upload_to='media/products', blank=True, null=True)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True, null=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.name)

	def form_valid(self, form):
		form.instance.commentor = self.request.user
		return super().form_valid(form)


