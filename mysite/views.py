from django.shortcuts import render, redirect

# Create your views here.
from mysite import models


def session_judge(request):
    username_session = request.session.get('username')
    password_session = request.session.get('password')
    users = models.UserInfo.objects.filter(username=username_session, password=password_session)
    return users.count()


def index(request):
    return render(request, 'index.html')


# 不返回页面,仅仅是处理登录的业务逻辑并且重定向;不然的话就是直接交到userList的页面进行业务逻辑的处理,这个的话
# 会使得userList更混乱(userList的话本身也有提交的post请求的)
def handle_index(request):
    username_index = str(request.POST.get('username_index')).strip()
    password_index = str(request.POST.get('password_index')).strip()
    if username_index != '' and username_index != None and password_index != '' and password_index != None:
        users = models.UserInfo.objects.filter(username=username_index, password=password_index)
        if users.count() > 0:
            request.session['username'] = username_index
            request.session['password'] = password_index
            request.session.set_expiry(120)
            return redirect(to='/userList/', request=request)
        else:
            return render(request, 'error_login.html')
    else:
        return render(request, 'error_login.html')


def userList(request):
    count = session_judge(request)
    if count > 0:
        user_list = list(models.UserInfo.objects.all())
        return render(request, 'userList.html', {'data': user_list})


def userList_add(request):
    count = session_judge(request)
    if count > 0:
        username_add = str(request.POST.get('username_add')).strip()
        password_add = str(request.POST.get('password_add')).strip()
        if username_add != '' and username_add != None and password_add != '' and password_add != None:
            models.UserInfo.objects.create(username=username_add,password=password_add)
            user_list = list(models.UserInfo.objects.all())
            return render(request,'userList.html',{'data':user_list})
        else:
            return render(request,'error_input.html')
    else:
        return render(request,'error_login.html')


def userList_delete(request):
    count = session_judge(request)
    if count > 0:
        username_delete = str(request.POST.get('username_delete')).strip()
        password_delete = str(request.POST.get('password_delete')).strip()
        if username_delete != '' and username_delete != None and password_delete != '' and password_delete != None:
            users = models.UserInfo.objects.filter(username=username_delete,password=password_delete)
            if users.count() >0:
                models.UserInfo.objects.filter(username=username_delete, password=password_delete).delete()
                user_list = list(models.UserInfo.objects.all())
                return render(request, 'userList.html', {'data': user_list})
            else:
                return render(request,'error_input.html')
        else:
            return render(request,'error_input.html')
    else:
        return render(request,'error_login.html')



