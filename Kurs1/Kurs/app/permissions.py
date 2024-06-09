
#чтобы посылкам мог переходить ток админ
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
def add_newpost_permission(sender, **kwargs):
    """Создает разрешение 'can_add_post' для приложения 'app'."""
    Permission.objects.get_or_create(
        codename='can_add_post',
        name='Может добавлять статьи',
        content_type=ContentType.objects.get_for_model(Blog)
    )

class YourAppConfig(AppConfig):
    name = 'app'
    
    def ready(self):
        post_save.connect(add_newpost_permission, sender=self.get_model('Blog'))





def add_add_product_permission(sender, **kwargs):
    """Создает разрешение 'can_add_product' для приложения 'app'."""
    Permission.objects.get_or_create(
        codename='can_add_product',
        name='Может добавлять продукты',
        content_type=ContentType.objects.get_for_model(Product)
    )

class YourAppConfig(AppConfig):
    name = 'app'
    
    def ready(self):
        post_save.connect(add_add_product_permission, sender=self.get_model('Product'))

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('app.can_add_post')
def newpost(request):

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('app.can_add_product')
def add_product(request):