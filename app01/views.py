from django.shortcuts import render, redirect,HttpResponse,reverse
from app01 import models
import time
# Create your views here.
from functools import wraps
def author_del2(request):
    return render(request, 'detail.html')


def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user=='alex' and pwd=='123':
            url=request.GET.get('url')
            if url:
                return_url =url
            else:
                return_url=reverse('publish')
            ret = redirect(return_url)
            ret.set_cookie('is_login', '1')
            return ret
        else:
            error='用户名或者密码错误'
    return render(request, 'login1.html', locals())



def login_required(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        #print(request.COOKIES)
        is_login = request.COOKIES.get('is_login')
        if is_login != '1':
            return redirect('/login/?url={}'.format(request.path_info))
        ret=func(request,*args,**kwargs)
        return ret
    return inner



def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)  # 要被装饰的对象
        print('执行的时间是：{}'.format(time.time() - start))
        return ret

    return inner


@timer  # 装饰器
def publish_list(request):
    # 获取出版社信息
    all_publish = models.Publisher.objects.all().order_by('id')
    # for i in all_publish:
    #     print(i.id)
    #     print(i.name)


    return render(request, 'publish.html', {'xxxxxx': all_publish})  # 骚操作



from django.views import View
from django.utils.decorators import method_decorator


@method_decorator(timer, name='dispatch')
class Publisher_add(View):
    # @method_decorator(timer)
    # def dispatch(self, request, *args, **kwargs):
    #     ret=super().dispatch(request,*args,**kwargs)
    #     return ret

    # @method_decorator(timer)
    def get(self, request):
        return render(request, 'publish_add.html')

    def post(self, request):
        pub_name = request.POST.get('pub_name')
        print(pub_name)
        if models.Publisher.objects.filter(name=pub_name):
            return render(request, 'publish_add.html', {'error': "出版社名称已经存在"})
        # add database
        ret = models.Publisher.objects.create(name=pub_name)
        print(ret)
        # 返回
        return redirect('/publish/')


# def publish_list_add(request):
#     # post request
#     if request.method == 'POST':
#         pub_name = request.POST.get('pub_name')
#         print(pub_name)
#         if models.Publisher.objects.filter(name=pub_name):
#             return render(request, 'publish_add.html', {'error': "出版社名称已经存在"})
#         # add database
#         ret = models.Publisher.objects.create(name=pub_name)
#         print(ret)
#         # 返回
#         return redirect('/publish/')
#     return render(request, 'publish_add.html')


def publish_del(request):
    # 获取要删除的id
    pk = request.GET.get('pk')
    # 根据pk到数据库进行删除
    models.Publisher.objects.get(pk=pk).delete()
    return redirect('/publish/')


def publish_edit(request):
    # get 返回一个页面，，页面包含form表单 imput有原始的数据
    pk = request.GET.get('pk')
    pub_obj = models.Publisher.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'publish_edit.html', {'pub_obj': pub_obj})
    else:
        pub_name = request.POST.get('pub_name')
        pub_obj.name = pub_name  # 只是在内存进行了修改
        pub_obj.save()  # 将修改操作提交给数据库
        return redirect('/publish/')

@login_required
def book_list(request):
    all_books = models.book.objects.all()
    # for i in all_books:
    #     print(i.name)
    #     print(i.pk)
    #     print(i.publisher,i.publisher.name) #关联的对象
    return render(request, 'book.html', {'all_books': all_books})


def book_add(request):
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        if not book_name:
            all_publishers = models.Publisher.objects.all()
            return render(request, 'book_add.html', {'all_pulishers': all_publishers, 'error': '书名不能为空'})

        # 将数据插入到数据库中
        models.book.objects.create(name=book_name, publisher_id=pub_id)
        return redirect('/book/')

    all_publishers = models.Publisher.objects.all()
    return render(request, 'book_add.html', {'all_publishers': all_publishers})


def book_del(request):
    # 获取用户提交的要删除数据的id
    pk = request.GET.get('id')
    models.book.objects.filter(pk=pk).delete()
    # 获取要删除的对象，删除
    # 重定向
    return redirect('/book/')


def book_edit(request):
    pk = request.GET.get('id')
    book_obj = models.book.objects.get(pk=pk)

    # post 请求
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        # 方式一  全部更新数据库
        # book_obj.name=book_name
        #
        # book_obj.publisher_id=pub_id
        # #book_obj.publisher=models.Publisher.objects.get(pk=pub_id)
        # book_obj.save() #保存到数据库中
        # 方式二 只修改需要修改的项
        models.book.objects.filter(pk=pk).update(name=book_name, publisher_id=pub_id)
        return redirect('/book/')
    # get 请求
    # 查询id
    # 查到对象
    # 返回页面，含有原始数据

    all_publishers = models.Publisher.objects.all()
    return render(request, 'book_edit.html', {'book_obj': book_obj, 'all_publishers': all_publishers})

@login_required
def book_pic(request):
    return render(request, 'book_pic.html')


@login_required
def author(request):
    # 查询所有作者
    all_authors = models.author.objects.all()
    for author in all_authors:
        print(author.books)  # 关系管理对象
        print(author.books.all())  # 关联的所有对象
    # 返回页面，包含作者名
    return render(request, 'author.html', {'all_authors': all_authors})


def author_add(request):
    if request.method == 'POST':
        # 获取用户数据
        book_name = request.POST.get('author_name')
        book_id = request.POST.getlist('book_id')  # 获取多个数据
        author_obj = models.author.objects.create(name=book_name)
        # 作者和书籍绑定多对多的关系
        author_obj.books.set(book_id)
        return redirect('/author/')

    # get
    # 查询所有书籍
    all_books = models.book.objects.all()
    # 返回一个表单，包含form表单，让用户输入作者姓名，选择作品
    return render(request, 'author_add.html', {'all_books': all_books})


def author_del(request):
    pk = request.GET.get('pk')
    # 删除的是作者和对应关系，并不包括书籍
    models.author.objects.filter(pk=pk).delete()
    return redirect('/author/')


def author_edit(request):
    pk = request.GET.get('id')
    author_obj = models.author.objects.get(pk=pk)

    # post
    # 获取用户提交的数据
    # 修改数据
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        book_id = request.POST.getlist('book_id')
        author_obj.name = author_name
        author_obj.save()
        # 修改作者和书的多对多的关系
        author_obj.books.set(book_id)

        return redirect('/author/')

    all_books = models.book.objects.all()
    return render(request, 'author_edit.html', {'author_obj': author_obj, 'all_books': all_books})


def mom(request):
    return render(request, 'mom.html')




from django.views import generic
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from helpers import get_page_list, ajax_required


class VideoDetailView(generic.DetailView):
    model = models.Video
    template_name = 'detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)

        # recommend_list = models.Video.objects.get(pk=pk)
        #
        # context['recommend_list'] = recommend_list
        return context










import logging
import smtplib

import datetime
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import *
from django.template.loader import render_to_string
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from helpers import get_page_list, AdminUserRequiredMixin, ajax_required, SuperUserRequiredMixin, send_html_email
# from .models import MyChunkedUpload

logger = logging.getLogger('my_logger')


class AddVideoView(TemplateView):
    template_name = 'video_add.html'

class MyChunkedUploadView(ChunkedUploadView):

    model = models.MyChunkedUpload
    print('hha')
    field_name = 'the_file'

class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = models.MyChunkedUpload

    def on_completion(self, uploaded_file, request):
        print('uploaded--->', uploaded_file.name)
        pass

    def get_response_data(self, chunked_upload, request):
        video = models.Video.objects.create(file=chunked_upload.file)
        return {'code': 0, 'video_id': video.id, 'msg': 'success'}

from . import forms


class VideoPublishView(generic.UpdateView):
    model = models.Video
    form_class = forms.VideoPublishForm
    template_name = 'video_publish.html'

    def get_context_data(self, **kwargs):
        context = super(VideoPublishView, self).get_context_data(**kwargs)
        # clf_list = Classification.objects.all().values()
        # clf_data = {'clf_list':clf_list}
        # context.update(clf_data)
        return context
    def get_success_url(self):
        return reverse('video_publish_success')


class VideoPublishSuccessView(generic.TemplateView):
    template_name = 'video_publish_success.html'

class VideoListView(AdminUserRequiredMixin, generic.ListView):
    model = models.Video
    template_name = 'video_list.html'
    context_object_name = 'video_list'
    paginate_by = 10
    q = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context



class IndexView(AdminUserRequiredMixin, generic.View):
    """
    总览数据
    """

    def get(self, request):
        video_count = models.Video.objects.get_count()
        video_has_published_count = models.Video.objects.get_published_count()
        video_not_published_count = models.Video.objects.get_not_published_count()

        data = {"video_count": video_count,
                "video_has_published_count": video_has_published_count,
                "video_not_published_count": video_not_published_count}
        return render(self.request, 'index.html', data)




