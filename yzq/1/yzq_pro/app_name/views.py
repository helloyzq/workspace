from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
import json
from django.views.decorators.csrf import csrf_exempt
from app_name.models import Passport,Address
from django.http import HttpResponse, JsonResponse
from utils.decorators import login_required
from order.models import OrderInfo, OrderGoods

# Create your views here.

def register(request):
    '''显示用户注册页面'''
    return render(request, 'app_name/register.html')

@csrf_exempt
def register_handle(request):
    # '''进行用户注册处理'''
    # # 接收数据
    # username = request.POST.get('user_name')
    # password = request.POST.get('pwd')
    # email = request.POST.get('email')

    data = json.loads(request.body.decode('utf-8'))
    username=data.get('username')
    password=data.get('password')
    email=data.get('email')

    # 进行数据校验
    if not all([username, password, email]):
        # 有数据为空
        # return render(request, 'app_name/register.html', {'errmsg':'参数不能为空!'})
        return JsonResponse({'code':2})

    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        # return render(request, 'app_name/register.html', {'errmsg':'邮箱不合法!'})
        return JsonResponse({'code':3})

    # 检测是否重复注册
    repeated=Passport.objects.get_one_passport(username=username,password=password)
    if repeated:
        # return render(request,'app_name/register.html',{'errmsg':'重复注册'})
        return JsonResponse({'code':2})

    # 进行业务处理:注册，向账户系统中添加账户
    # Passport.objects.create(username=username, password=password, email=email)
    passport = Passport.objects.add_one_passport(username=username, password=password, email=email)

    # 注册完，返回登录页。
    # return redirect(reverse('app_name:login'))
    return JsonResponse({'code':200})

def login(request):

    return render(request,'app_name/login.html')

@csrf_exempt
def login_check(request):
    # username=request.POST.get('username')
    # password=request.POST.get('pwd')

    data=json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    remember = data.get('remember')

    if not all([username,password]):
        if not username:
            # return render(request,'app_name/login.html',{'errmsg':'用户名不能为空'})
            return JsonResponse({'code':2})
        # return render(request,'app_name/login.html',{'errmsg':'密码错误'})
        return JsonResponse({'code':3})

    passport=Passport.objects.get_one_passport(username=username, password=password)
    if passport:
        # 用户名密码正确
        # 跳到books的views里面的index函数
        # return redirect(reverse('books:index'))

        # 记住用户的登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id

        jres= JsonResponse({'code':200})
        # 判断是否需要记住用户名
        if remember == 'true':
            # 记住用户名
            jres.set_cookie('username', username, max_age=7 * 24 * 3600)
        else:
            # 不要记住用户名
            jres.delete_cookie('username')
        return jres

    else:
        # 用户名或密码错误
        # return render(request,'app_name/login.html',{'errmsg':'用户名密码错误'})
        return JsonResponse({'code':4})

@login_required
def user(request):
    '''用户中心-信息页'''
    # print(request.session._get_session())
    passport_id = request.session.get('passport_id')
    # 获取用户的基本信息
    addr = Address.objects.get_default_address(passport_id=passport_id)
    books_li = []
    context = {
        'addr': addr,
        'book_id':passport_id,
        'page': 'user',
        'books_li': books_li
    }
    return render(request, 'app_name/user_center_info.html', context)

@login_required
def address(request):
    '''用户中心-地址页'''
    # 获取登录用户的id
    passport_id = request.session.get('passport_id')
    if request.method == 'GET':
        # 显示地址页面
        # 查询用户的默认地址
        addr = Address.objects.get_default_address(passport_id=passport_id)
        return render(request, 'app_name/user_center_site.html', {'addr': addr, 'page': 'address'})
    else:
        # 添加收货地址
        # 1.接收数据
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')

        # 2.进行校验
        if not all([recipient_name, recipient_addr, zip_code, recipient_phone]):
            return render(request, 'app_name/user_center_site.html', {'errmsg': '参数不必为空!'})

        # 3.添加收货地址
        Address.objects.add_one_address(passport_id=passport_id,
                                        recipient_name=recipient_name,
                                        recipient_addr=recipient_addr,
                                        zip_code=zip_code,
                                        recipient_phone=recipient_phone)

        # 4.返回应答
        return redirect(reverse('app_name:address'))


@login_required
def order(request):
    '''用户中心-订单页'''
    # 查询用户的订单信息
    passport_id = request.session.get('passport_id')

    # 获取订单信息
    order_li = OrderInfo.objects.filter(passport_id=passport_id)

    # 遍历获取订单的商品信息
    # order->OrderInfo实例对象
    for order in order_li:
        # 根据订单id查询订单商品信息
        order_id = order.order_id
        order_books_li = OrderGoods.objects.filter(order_id=order_id)

        # 计算商品的小计
        # order_books ->OrderBooks实例对象
        for order_books in order_books_li:
            count = order_books.count
            price = order_books.price
            amount = count * price
            # 保存订单中每一个商品的小计
            order_books.amount = amount

        # 给order对象动态增加一个属性order_books_li,保存订单中商品的信息
        order.order_books_li = order_books_li

    context = {
        'order_li': order_li,
        'page': 'order'
    }

    return render(request, 'app_name/user_center_order.html', context)
