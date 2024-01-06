from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp.")
        return password2


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name="cateories", null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self) :
        return self.name
class Product(models.Model):
    category =  models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name