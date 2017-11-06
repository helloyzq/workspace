from django.conf.urls import url
from .views import test,sy
urlpatterns = [
    url(r'^index1/', test),
    url(r'^sy/', sy),
]
