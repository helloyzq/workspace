from django.shortcuts import render

# Create your views here.
def test(request):

    return render(request,'app1/index.html')

def sy(request):
    return render(request,'app1/index1.html')

