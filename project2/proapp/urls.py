from django.conf.urls import url
from .views import test,test1,times,test3,test4,test2,test5
urlpatterns = [
    # 表单
    url(r'^index1/',test2),
    url(r'^index21/',test5),

    url(r'^test/',test),
    url(r'^test3/',test3),
    # 重定向
    url(r'^test1$',test1),
    url(r'^times/',times),
    # static
    url(r'^test4/',test4),
]