from django.conf.urls import url
from .views import test
urlpatterns = [
    url(r'^(?P<abc>\d{4})/',test),
]