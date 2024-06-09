"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from app.cart import Cart





# Create your models here.
class Blog(models.Model):
    id = models.AutoField(primary_key=True)

   

    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")


    description = models.TextField(verbose_name = "Краткое содержание")


    content = models.TextField(verbose_name = "Полное содержание")


    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")


    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    
    image = models.FileField(default='temp.jpg', verbose_name = 'Путь к картинке' )
    #Методы класса:
        
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args [str(self.id)])

    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title
        #Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в нодели (*-* означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статья блог
        verbose_name_plural = "статьи блога" # то не для всех статей блога
        
admin.site.register(Blog)


class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Статья удалена")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")
    id = models.BigAutoField(primary_key=True)
    #Методы класса
    def str(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
admin.site.register(Comment)




class Category(models.Model):
    name = models.CharField(max_length=255)
    id = models.BigAutoField(primary_key=True)



class Product(models.Model):
    # Ваши поля для товара
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скидка", default=0, null=True, blank=True)
    id = models.BigAutoField(primary_key=True)
     # Первое изображение
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # Дополнительные изображения
    additional_images = models.ManyToManyField('ProductImage', blank=True, related_name='product')

    
    floors = models.IntegerField(verbose_name="Этажи", default=None, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Площадь", default=0, null=True)
    
    materials = models.CharField(max_length=255, verbose_name="Материалы", default='', null=True)

    def __str__(self):
        return self.name
admin.site.register(Product)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', default='no_image.png')
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartItem')
    id = models.BigAutoField(primary_key=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    id = models.BigAutoField(primary_key=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('Product', through='OrderItem')
    id = models.BigAutoField(primary_key=True)
    STATUS_CHOICES = (
        ('created', 'Заказ создан'),
        ('ready', 'Готов к выдаче'),
        ('canceled', 'Отменен'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    address = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=20, default='')

    def __str__(self):
        return f'Order {self.id} - {self.status}'
admin.site.register(Order)
    # Добавьте другие поля, которые вам нужны для заказа

 


class OrderItem(models.Model):  # Добавим определение OrderItem
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    id = models.BigAutoField(primary_key=True)

