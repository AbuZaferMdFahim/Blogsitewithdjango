from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import (Blog,Tag,Category)  

def home(request):
    blogs = Blog.objects.order_by('-created')
    tags = Tag.objects.order_by('-created')
    context = {"blogs": blogs,"tags": tags}
    return render(request,'home.html',context)

def blogs(request):
    queryset = Blog.objects.order_by('-created')
    tags = Tag.objects.order_by('-created')
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,2)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs,"tags": tags, "paginator": paginator}
    return render(request, 'blogs.html',context)

def category_blogs(request,slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by('created')[:4]
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 2)
    recentblogs = Blog.objects.order_by('-created')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs, "tags": tags, "recentblogs": recentblogs}
    return render(request, 'category_blogs.html',context)

def tag_blogs(request,slug):
    tags = get_object_or_404(Tag, slug=slug)
    queryset = tags.tag_blogs.all()
    tags = Tag.objects.order_by('created')[:4]
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 2)
    recentblogs = Blog.objects.order_by('-created')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs, "tags": tags, "recentblogs": recentblogs}
    return render(request, 'tag_blogs.html',context)

def blog_details(request,slug):
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id = blog.category.id)
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('created')[:4]

    context = {"blog": blog, "related_blogs": related_blogs, "tags": tags}
    return render(request, 'blog_details.html', context)
