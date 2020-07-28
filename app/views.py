from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.

from django.views.generic.list import ListView
from . models import Blog
from django.views.generic.detail import DetailView

class index(ListView):
    template_name = 'index.html'  #어떤 html이랑 연결?
    context_object_name = 'blog_list'    #모델이랑 연결시키고 모델을 다 불러오겠다?
    def get_queryset(self):
        return Blog.objects.all  #blog애들 가져와서 그 이름을 blog_list 라고 하겠다

class detail(DetailView):
    model = Blog
    template_name = 'detail.html'
    context_object_name = 'blog'  #불러온 모델을 거기에서 어떤 이름으로 쓸거냐??
    

class delete(DeleteView):
    model = Blog
    template_name = 'delete.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('index')

class update(UpdateView):
    model = Blog
    template_name = 'update.html'
    fields = ['title', 'text']  # 불러오고 싶은 거만 불러올 수 있음/ 모델 불러오고 어떤 필드를 쓸거냐 시간은 안 쓰니까 안 들고옴
    success_url = reverse_lazy('index')
    #성공하면 가는 url

class create(CreateView):
    model = Blog
    template_name = 'create.html'
    fields= ['title', 'text']

    def form_valid(self,form):        #author 가 로그인한 나랑 똑같은지
        Blog = form.save(commit=False)
        Blog.author = self.request.user
        Blog.save()

        return HttpResponseRedirect(self.request.POST.get('next','/'))

def result(request):
    BlogPosts = Blog.objects.all()
    query = request.GET.get('query','')

    if query:     #쿼리 있으면 가져오고 없으면 안 가져옴 쿼리는 아까 name이 쿼리   // text__icontains -> 쿼리가 최슬옹 중 최만 있어도 한글자만들어있어도 가져오겠다
        #쿼리 대신에 '가' 쓰면 '가'가 든 거 가져옴
        BlogPosts = BlogPosts.filter(Q(title__icontains=query)| Q(text__icontains=query) | Q(author__username__icontains = query)).order_by('-time')

        
    #블로그 포스트를 필터를 걸어서 정의할 것이다!!  --> 검색
    return render(request, 'result.html',{'BlogPosts':BlogPosts, 'query':query })   #어디로 보내냐 