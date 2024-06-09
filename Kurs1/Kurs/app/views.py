


"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .models import Category, Product
from django.db import models
from django.shortcuts import render
from .models import Category, Product
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from .forms import AddToCartForm
from django.shortcuts import render, redirect, get_object_or_404
from app.cart import Cart
from app.models import Product
from app.models import Product, Order
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order
from .models import OrderItem
from django.http import JsonResponse
from .cart import Cart
from .models import Product
from django.urls import reverse


from.forms import BlogForm
from.models import Blog

from.models import Comment # использование модели комментариев

from.forms import CommentForm # использование формы ввода комментария
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с моими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'магазины',
            'year':datetime.now().year,
        }
    )
def anketa(request):
    assert isinstance(request,HttpRequest)
    data = None
    gender = {'1':'Мужской','2':'Женский'}
    tehnik={'1':'Каждый день','2':'Несколько раз в недлю','3':'Несколько раз в месяц'}
    if request.method == 'POST':
        form=AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['disain'] = form.cleaned_data['disain']
            data['tehnik'] = tehnik[form.cleaned_data['tehnik']]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['polza'] = form.cleaned_data['polza']
            data['nedostatki'] = form.cleaned_data['nedostatki']
            form=None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data,
        }
    )

def registration(request):
    """Renders the registration page."""

    

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации


            reg_f.save() # сохраняем изменения после добавления данных


            return redirect('home') # переадресация на главную страницу после регистрации

    else:

        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    assert isinstance(request, HttpRequest)
    return render(

     request,

     'app/registration.html',

      {

         'regform': regform, # передача формы в шаблон веб-страницы

          'year':datetime.now().year,

      }

    )

def blog(request):

    """Renders the blog page."""

    assert isinstance(request, HttpRequest)

    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели

    return render(

        request,

        'app/blog.html',

        {

            'title':'Блог',

            'posts': posts, # передача списка статей в шаблон веб-страницы

            'year':datetime.now().year,

        }

)
def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

#декоратор только админ может зайти на создать пост

def is_admin(user):
    if not user.is_superuser:
        raise PermissionDenied  # Выбрасываем исключение PermissionDenied
    return True

@login_required
@user_passes_test(is_admin)


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',

            'year':datetime.now().year,
        }
    )
def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def catalog(request):
    categories = Category.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()
    products = Product.objects.all()  # Замените на вашу модель товара
    cart = Cart(request)
    for product in products:
        product.cart_quantity = cart.get_quantity(product.id)
        if product.discount:
            product.discounted_price = product.price * (1 - product.discount / 100)
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)#поисковая строка

    for product in products:
        product.cart_quantity = cart.get_quantity(product.id)

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'app/catalog.html', context)



@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(request, 'app/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = AddToCartForm()

    if product.discount:
        discounted_price = product.price * (1 - product.discount / 100)
    else:
        discounted_price = None

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('cart')

    return render(request, 'app/product_detail.html', {'product': product, 'form': form, 'discounted_price': discounted_price})

@login_required
def view_cart(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'app/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product_id=product_id)  # Передаем product_id
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart')

def decrement_item(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product)
    return redirect(reverse('view_cart'))

def increment_item(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.increment(product)
    return redirect(reverse('view_cart'))
from django.core.mail import send_mail  # Импорт send_mail
from django.conf import settings

def create_order(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()  # Сохраняем заказ с информацией о доставке
            send_mail(
            "Заказ",
            "Message." f' заказ №{order.id} успешно оформлен.'
            f' Адрес доставки: {order.address}'
            f' Имя: {order.name}'
            f' Почта: {order.email}'
            f' Телефон: {order.phone_number}'
            f' Товары в заказе {order.name}'
            ,
            "sobo754sava@yandex.ru",
            ["sobo754sava@yandex.ru", "sobo754sava@yandex.ru"],
)

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])

            cart.clear()
            return redirect('my_orders')
    else:
        form = OrderForm()

    return render(request, 'app/create_order.html', {'form': form, 'cart': cart})
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/my_orders.html', {'orders': orders})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Проверяем, что пользователь, пытающийся отменить заказ, является владельцем заказа
    if request.user == order.user:
        order.status = 'canceled'
        order.save()
    
    return redirect('my_orders')



def is_manager_or_admin(user):
    return user.groups.filter(name__in=['menedger', 'admin']).exists()

@login_required
@user_passes_test(is_manager_or_admin)


def all_orders(request):
    orders = Order.objects.all()

    for order in orders:
        total_price = 0
        for item in order.orderitem_set.all():
            if item.product.discount is not None and item.product.discount > 0:
                # Вычисляем цену со скидкой для товара
                item.discounted_price = item.product.price * (1 - item.product.discount / 100)
                total_price += item.quantity * item.discounted_price
            else:
                # Если скидки нет, используем обычную цену товара
                total_price += item.quantity * item.product.price
        
        order.total_price = total_price  # Сохраняем общую стоимость заказа

    return render(request, 'app/all_orders.html', {'orders': orders})

def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

    return redirect('all_orders')

# views.py









