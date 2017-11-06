#conding:utf-8
from django.shortcuts import render,HttpResponse
# Create your views here.
def test(request,abc):
    id=request.GET.get("id")
    name=request.GET.get("name")
    content={"id":id,"name":name}
    return render(request,"index.html",{"abc":abc,"id":id,"name":name})