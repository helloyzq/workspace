from django.conf.urls import url
from .views import test1
urlpatterns = [
    url(r'^test1/', test1),
]