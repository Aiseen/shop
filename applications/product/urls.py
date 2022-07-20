from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import CategoryView, ProductView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('',ProductView)


urlpatterns = [
    # path('category/', CategoryView.as_view({'get': 'list'})),
    path('', include(router.urls)),


]