from django.shortcuts import render,HttpResponse,HttpResponseRedirect
# from django.template import loader,RequestContext
# Create your views here.
def test2(request):
    return render(request,'templateUrls/index1.html')
def test5(request):
    uname=request.POST['uname']
    upwd=request.POST['upwd']
    ugender=request.POST['ugender']
    uhobby=request.POST.getlist('uhobby')
    cont={"uname":uname,"upwd":upwd,"ugender":ugender,"uhobby":uhobby}
    return render(request,"templateUrls/index21.html",cont)


def test4(request):
    return render(request,'templateUrls/index4.html')



def test3(request):
    # dict
    mydict={"key-a":"values-a","key-b":"values-b","key-c":"values-c"}
    # list
    mylist=['西游记','三国演义','老人与海']
    return render(request,'templateUrls/yzqqwe.html',{"x":mydict,"y":mylist})



def test1(request):
    return HttpResponseRedirect('times/')
def times(request):
    return HttpResponse("这是重定向的目的啊？？？？")


def test(request):
    request.session['var1']='abc'
    request.session['var2']='axv'
    c=request.session['var1']
    d=request.session['var2']
    context={"c":c,"d":d}
    del request.session['var1']
    context["e"]=request.session.get("var1")
    context["f"]=request.session.get("var2")
    request.session['var1'] = 'abc'
    request.session.flush()
    context["a"]=request.session.get("var1")
    context["b"]=request.session.get("var2")
    return render(request,'templateUrls/index.html',context)
