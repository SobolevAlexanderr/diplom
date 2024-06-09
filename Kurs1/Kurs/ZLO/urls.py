"""
Definition of urls for ZLO.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import path

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.urls import path





urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('registration/', views.registration, name='registration'),
    path('anketa/', views.anketa, name='anketa'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost', views.newpost, name='newpost'),
    path('videopost', views.videopost, name='videopost'),
    path('catalog/', views.catalog, name='catalog'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='cart'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('accounts/login/', views.registration, name='login'),
    path('my_orders/', views.my_orders, name='my_orders'),  # Создайте отдельный вид для просмотра заказов пользователя
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('decrement_item/<int:product_id>/', views.decrement_item, name='decrement_item'),
    path('increment_item/<int:product_id>/', views.increment_item, name='increment_item'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    

    path('all_orders/', views.all_orders, name='all_orders'),
    # Другие URL-пути
    path('login/',


         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()